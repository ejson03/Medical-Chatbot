# Chatbot Widget designed for Rasa Bots 🤖

An Open Source ChatBot widget easy to connect to RASA bot through [Rest](https://rasa.com/docs/rasa/user-guide/connectors/your-own-website/#rest-channels) Channel.


![forthebadge](https://forthebadge.com/images/badges/built-with-love.svg)
[![forthebadge](https://forthebadge.com/images/badges/for-you.svg)](https://forthebadge.com)

[![forthebadge](https://forthebadge.com/images/badges/made-with-javascript.svg)](https://forthebadge.com)
[![forthebadge](https://forthebadge.com/images/badges/uses-html.svg)](https://forthebadge.com)
[![forthebadge](https://forthebadge.com/images/badges/uses-css.svg)](https://forthebadge.com)

[![forthebadge](https://forthebadge.com/images/badges/built-with-swag.svg)](https://forthebadge.com)
[![forthebadge](https://forthebadge.com/images/badges/check-it-out.svg)](https://forthebadge.com)

[![forthebadge](https://forthebadge.com/images/badges/makes-people-smile.svg)](https://forthebadge.com)

## Features

- [Text Messages](https://github.com/JiteshGaikwad/Chatbot-Widget/blob/d1d331f19bc6d5e74b85a16faaeff2ccdf8bfceb/static/js/script.js#L198)
- [Buttons](https://github.com/JiteshGaikwad/Chatbot-Widget/blob/d1d331f19bc6d5e74b85a16faaeff2ccdf8bfceb/static/js/script.js#L211)
- [Images](https://github.com/JiteshGaikwad/Chatbot-Widget/blob/d1d331f19bc6d5e74b85a16faaeff2ccdf8bfceb/static/js/script.js#L204)
- [Quick Replies](https://github.com/JiteshGaikwad/Chatbot-Widget/blob/d1d331f19bc6d5e74b85a16faaeff2ccdf8bfceb/static/js/script.js#L219)
- [Cards Carousel](https://github.com/JiteshGaikwad/Chatbot-Widget/blob/d1d331f19bc6d5e74b85a16faaeff2ccdf8bfceb/static/js/script.js#L234)
- [Charts](https://github.com/JiteshGaikwad/Chatbot-Widget/blob/d1d331f19bc6d5e74b85a16faaeff2ccdf8bfceb/static/js/script.js#L241)
- [Collapsible](https://github.com/JiteshGaikwad/Chatbot-Widget/blob/d1d331f19bc6d5e74b85a16faaeff2ccdf8bfceb/static/js/script.js#L262)
- [Bot Typing Indicator](https://github.com/JiteshGaikwad/Chatbot-Widget/blob/d1d331f19bc6d5e74b85a16faaeff2ccdf8bfceb/static/js/script.js#L490)
- [Location Acccess](https://github.com/JiteshGaikwad/Chatbot-Widget/blob/d1d331f19bc6d5e74b85a16faaeff2ccdf8bfceb/static/js/script.js#L444)
- [Conversation Restart](https://github.com/JiteshGaikwad/Chatbot-Widget/blob/d1d331f19bc6d5e74b85a16faaeff2ccdf8bfceb/static/js/script.js#L311)
- [Fully Customizable](https://github.com/JiteshGaikwad/Chatbot-Widget/blob/master/static/js/script.js)
- [DropDown](https://github.com/JiteshGaikwad/Chatbot-Widget/blob/58f685643ef5e70603147f99b7b1f5e35b73be0f/static/js/script.js#L226)
- [Video Message](https://forum.rasa.com/t/displaying-video-in-the-rasa-webchat/26931?u=jiteshgaikwad)


## Instructions
*Before you start your bot server, make sure you have added `rest` channel in the `credentials.yml` file*

**Step_1**: Start your Rasa bot server & action server(if you have custom actions) using the below command
> rasa run -m models --enable-api --cors "*" --debug

> rasa run actions 

**Step_2**: Once you have your Rasa server up & running, open the `index.html` file to test the bot.

## Screenshots:
![ScreenShot](https://github.com/JiteshGaikwad/Chatbot-Widget/blob/master/static/img/charts_1.png) ![ScreenShot](https://github.com/JiteshGaikwad/Chatbot-Widget/blob/master/static/img/collapse_1.png) 

![ScreenShot](https://github.com/JiteshGaikwad/Chatbot-Widget/blob/master/static/img/charts_2.png)

![ScreenShot](https://github.com/JiteshGaikwad/Chatbot-Widget/blob/master/static/img/menu.png)![ScreenShot](https://github.com/JiteshGaikwad/Chatbot-Widget/blob/master/static/img/collapse_1.png)

![ScreenShot](https://github.com/JiteshGaikwad/Chatbot-Widget/blob/master/static/img/ui_1.PNG)
![ScreenShot](https://github.com/JiteshGaikwad/Chatbot-Widget/blob/master/static/img/ui_2.PNG)
![ScreenShot](https://github.com/JiteshGaikwad/Chatbot-Widget/blob/master/static/img/chats.png) ![ScreenShot](https://github.com/JiteshGaikwad/Chatbot-Widget/blob/master/static/img/cardsUi_2.png) ![ScreenShot](https://github.com/JiteshGaikwad/Chatbot-Widget/blob/master/static/img/cardsUi.png)
![ScreenShot](https://github.com/JiteshGaikwad/Chatbot-Widget/blob/master/static/img/video_msg.PNG)



## Library used:
- [Materialize CSS](https://materializecss.com) for CSS
- [Chart.js](https://www.chartjs.org/) for Charts

## Demo:

Check out the widget in action here: https://youtu.be/mnolLtOWykk

