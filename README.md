#Docs for Htmailer.

Htmessage is simple extension of django's official EmailMessage.
It is adapted to work with django templating engine or any templating engine adapted to work with django. 

**Htmessage subclasses `Django.core.mail.EmailMessage`**
User defines instance of **Htmailer** like so
	`from htmailer import Htmessage ` 

	`message = Htmessage()`

	`message.subject('subject goes here')`
	`message.html_template('mail_html.html', context)`
	`message.txt_template('mail_text.html', context)` 

`'mail_*.html'` is a path to the template where the mail is defined.

This works like standard django Render() function, such that 'mail_*.html' is searched for in the dirs 
defined in the `TEMPLATE` setting Dictconfig.
Since this mailer extends `EmailMessage`, standard behaviour like `send()`, `header()` are available, 
that the content of rendered text template from the mailer is the body of the text message and manually setting `body()`
will replace the rendered text but will have no effect on the html part of the message.

#USAGE
`class Htmessage`
+ constructed like `Django.core.mail.EmailMessage`
	`html_template(template, context)`
+ `template` is a path to the html file containing the template.
+ `context` is a dictionary containing context data to replace the place holders in the html file.
`txt_template(template, context)`  works just like `html_template()` above.

The html file for txt template should not contain html document, its content should just be text with
with placeholders according to the style of the Template Engine used by your project

For example, the html file can contain;

	<html>
	<head>
		<title>Welcome to htmailer</title>
	</head>
	<body>
		Dear {{user_name}},<br>
			welcome to htmailer, I hope you wil find it useful one way or another.
																		signed,
																		{{company_name}}
	</body>
	</html>
 and the text file can contain the same information but as plain text like so;

	 Dear {{user_name}},
			welcome to htmailer, I hope you wil find it useful one way or another.
																		signed,
																		{{company_name}}.

This context for the html message above will be a `dict` like:

	{'user_name': 'dino', 'company_name': 'A cute company'}





