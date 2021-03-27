# Chatbot

## Instalation

In this project, we only worked in local mode.

first clone the repository in a new venv.

Then run:

```pip install -r requirement.txt```

In the shell of the repository of your project do:

```rasa run actions```

then in another shell:

```rasa run```

It should be runing on your port 5005.

Launch ngrok.exe. we need to open our port 5005 in order to make the connection between Facebook and our chatbot. In the ngrok shell do:

```ngrok http 5005```

Now your ngtok shell should look like this:

![image](https://user-images.githubusercontent.com/74590573/112733117-52831a00-8f3e-11eb-8a7d-8cf4e6a8c5bf.png)

Go to https://developers.facebook.com and create a new app using messenger. Link a page to your application.
Get your secret app token and your page access token, add copy paste them in the credential.yml file.

in your messenger parameters on facebook for developers, go to webhooks. Put the https address of ngrok followed by /webhooks/facebook/webhook as the URL and the verify of your credential.yml file as the password and verified. In your ngrok shell, you should have the message:

```GET /webhooks/facebook/webhook 200 OK ```

In your webhook's parameters, allow messages and messaging_postbacks.

You can now use your chatbot on your facebook page.

## How to use

Firstly, you can say hello to your bot. Then you you can ask for a Pokémon. Then you can ask its type, its location, its generation, if it is a legendary Pokémon, and a similar Pokémon.

Here an example of a conversation:

![image](https://user-images.githubusercontent.com/74590573/112734596-10120b00-8f47-11eb-9e06-a4d2ee10778f.png)
