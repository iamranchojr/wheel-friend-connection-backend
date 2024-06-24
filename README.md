# Wheel Friend Connection Backend
Wheel Friend Connection Backend: a FastAPI powered backend that allows users to connect with friends,
send and receive friend requests, and get live updates on friends' statuses.

### API Documentation
An OpenAPI documentation of the API can be found via the following url [here](https://wfc-backend-api-8bd958c0167d.herokuapp.com/docs). 

Below are instructions on how to run this API locally on your device using Docker.

### Getting started
Install docker desktop locally on your machine

To run the application, open a terminal in the project root directory and run the command below. 
Before doing that, make sure to have created a `.env` file with all the env variables required by 
the application. This is needed by docker to properly configure and run the application. 
There an .env.example file that will let you know what values are needed.

```
docker-compose up -d --build
```

This command will also build the container and install all necessary dependencies, so you do not have to do it manually.
And that is it, you can now access the docs and test out the APIs locally on your device.

To get the full experience of this API, you can find the corresponding frontend application [here](https://github.com/iamranchojr/wheel-friend-connection-frontend).

Contact me via [email](mailto:iamranchojr@gmail.com) if you have questions or seek clarifications.