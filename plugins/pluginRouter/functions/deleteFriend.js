import {sender} from "./baseClasses/sendClass";
import {util} from "./baseClasses/utilityClass";
import {service} from "./baseClasses/service";

class pluginClass extends service{
    constructor(){
        super(name);
    }

    __checkParameters(parameters){
        if(!parameters.parameters.project || !parameters.parameters.object || !parameters.values[0].friend){
            throw "Необходимо указать параметры 'проект', 'объект(пользователь)' и 'друг(пользователь)' для добавления друга."
        }
    }

    __getFilterForFriend(user, field, friend){
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
                filter: this.__getFilterForFriend(user, field, friend)
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

    __deleteFriend(project, user, friend){
        return sender.send({
            object: `${project}.friends`,
            method: "delete",
            parameters: {
                filter: this.__getFilterForFriend(user, "friendID", friend)
            }
        });
    }

    __deleteRequest(project, user, field, friend){
        return sender.send({
            object: `${project}.friendsRequests`,
            method: "delete",
            parameters: {
                filter: this.__getFilterForFriend(user, field, friend)
            }
        });
    }

    async run(parameters, token, deep = 0){
        this.__checkParameters(parameters);

        let {project, object} = parameters.parameters;
        let friend = parameters.values[0].friend;

        if (await this.__checkFriend(project, "friends", "friend", object, friend)) {
            await this.__deleteFriend(project, object, friend);
            await this.__deleteFriend(project, friend, object);
            await this.__addRequest(project, object, friend);
            await this.__addSentRequest(project, friend, object);
        }
        else if (!await this.__checkFriend(project, "friendsRequests", "sent_request", object, friend)){
            await this.__deleteRequest(project, object, "sent_request", friend);
        }
        else {
            throw "Невозможно удалить пользователя, которого нет ни в друзьях ни в заявках на добавление в друзья."
        }
    }
}

let name = "deleteFriend";
let plugin = new pluginClass();

export {
    plugin as plugin,
    name as name
}
