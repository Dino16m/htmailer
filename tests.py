from django.test import TestCase, override_settings
from .resolver import TestResolver
from .htmailer import Htmessage
from django.core import mail
import os


Test_Dir = os.path.dirname(os.path.abspath(__file__))

# Create your tests here.
class TestMailer(TestCase):
	def setUp(self):
		Resolver = TestResolver
		self.mailer = Htmessage(
			subject='Hello from a tester', from_email='hiz@dynasty.com', to=['them@dynasty.com'], bcc=None, 
			connection=None, attachments=None, headers=None, cc=None, 
			reply_to=None, Resolver=Resolver
		)

	def test_txt_template_renders(self):
		"""The path is never used because we added a dummy resolver."""
		self.mailer.txt_template(path='/path/to/nothing.html')
		self.assertEquals(self.mailer.get_txt_msg(), self.mailer.body)
		self.assertEquals(self.mailer.get_txt_msg(), TestResolver.TEST_MESSAGE)

	def test_html_template_renders(self):
		"""The path is never used because we added a dummy resolver."""
		self.mailer.html_template(path='/path/to/nothing.html')
		self.assertEquals(self.mailer.get_html_msg(), TestResolver.TEST_MESSAGE)

	def test_message_has_html(self):
		"""The path is never used because we added a dummy resolver."""
		self.mailer.html_template(path='/path/to/nothing.html')
		ht_alternative = self.mailer.alternatives[0]
		self.assertEquals(ht_alternative, (TestResolver.TEST_MESSAGE, "text/html"))

	
	@override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
	def test_msg_is_sent(self):
		self.mailer.txt_template(path='/path/to/nothing.html')
		self.mailer.html_template(path='/path/to/nothing.html')
		self.mailer.send()
		self.assertNotEqual(mail.outbox, [])
		this_mail = mail.outbox[0]
		self.assertEqual(this_mail.body, self.mailer.body)

class IntegrationTest(TestCase):


	TEMPLATES = [
		{
			'BACKEND': 'django.template.backends.django.DjangoTemplates',
			'DIRS': [os.path.join(Test_Dir, 'test_templates', 'messages')],
			'APP_DIRS': False,
			'OPTIONS': {
				'context_processors': [
					'django.template.context_processors.debug',
					'django.template.context_processors.request',
					'django.contrib.auth.context_processors.auth',
					'django.contrib.messages.context_processors.messages',
				],
			},
		},
	]

	@override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
	@override_settings(TEMPLATES=TEMPLATES)
	def test_real_send(self):
		message = Htmessage(
			subject='Hello from a tester', from_email='hiz@dynasty.com', to=['them@dynasty.com'], bcc=None, 
			connection=None, attachments=None, headers=None, cc=None, 
			reply_to=None
		)
		context = {'user_name': 'dino16m', 'company_name': 'Htmailer company'}
		message.txt_template('test_message_txt.html', context).html_template('test_message.html', context)
		message.send()
		sent_message = mail.outbox[0]
		self.assertEquals(sent_message.body, message.body)
		self.assertIn(context['user_name'], sent_message.body)
		self.assertIn(context['company_name'], sent_message.body)


