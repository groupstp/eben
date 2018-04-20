import {sender} from "./baseClasses/sendClass";
import {util} from "./baseClasses/utilityClass";
import {service} from "./baseClasses/service";

class pluginClass extends service{
    constructor(){
        super(name);
    }

    static __checkParameters(parameters){
        if(!parameters.parameters.project || !parameters.parameters.object || !parameters.values[0].friend){
            throw "Необходимо указать параметры 'проект', 'объект(пользователь)' и 'друг(пользователь)' для добавления друга."
        }
    }

    static __getFilterForFriend(user, field, friend){
        return {
            comparisons: {
                user: {
                    left: {
                        type: "field",
                        value: "userID"
                    },
                    right: {
                        type: "value",
                        value: user
                    },
                    sign: "equal"
                },
                friend: {
                    left: {
                        type: "field",
                        value: field
                    },
                    right: {
                        type: "value",
                        value: friend
                    },
                    sign: "equal"
                }
            },
            tree: {
                and: ["user", "friend"]
            }
        }
    }

    __checkFriend(project, object, field, user, friend){
        return sender.send({
            object: `${project}.${object}`,
            method: "get",
            parameters: {
                filter: pluginClass.__getFilterForFriend(user, field, friend)
            }
        });
    }

    __addSentRequest(project, user, friend){
        return sender.send({
            object: `${project}.friendsRequests`,
            method: "insert",
            parameters: {
                values: {
                    userID: user,
                    sent_request: friend
                }
            }
        });
    }

    __addRequest(project, user, friend){
        return sender.send({
            object: `${project}.friendsRequests`,
            method: "insert",
            parameters: {
                values: {
                    userID: user,
                    request: friend
                }
            }
        });
    }

    __addFriend(project, user, friend){
        return sender.send({
            object: `${project}.friends`,
            method: "insert",
            parameters: {
                values: {
                    userID: user,
                    friendID: friend
                }
            }
        });
    }

    __deleteRequest(project, user, field, friend){
        return sender.send({
            object: `${project}.friendsRequests`,
            method: "delete",
            parameters: {
                filter: pluginClass.__getFilterForFriend(user, field, friend)
            }
        });
    }

    async run(parameters, token, deep = 0){
        pluginClass.__checkParameters(parameters);

        let {project, object} = parameters.parameters;
        let friend = parameters.values[0].friend;

        if (await this.__checkFriend(project, "friends", "friend", object, friend)) {
            throw "Невозможно добавить в друзья человека, который уже в друзьях.";
        }
        else if (await this.__checkFriend(project, "friendsRequests", "request", object, friend)) {
            await this.__deleteRequest(project, object, "request", friend);
            await this.__deleteRequest(project, friend, "sent_request", object);
            await this.__addFriend(project, object, friend);
            await this.__addFriend(project, friend, object);
        }
        else if (!await this.__checkFriend(project, "friendsRequests", "sent_request", object, friend)){
            throw "Заявка на добавление в друзья уже существует.";
        }
        else {
            await this.__addSentRequest(project, object, friend);
            await this.__addRequest(project, friend, object);
        }
    }
}

let name = "addFriend";
let plugin = new pluginClass();

export {
    plugin as plugin,
    name as name
}
