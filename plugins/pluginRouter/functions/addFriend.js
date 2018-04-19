import {sender} from "./baseClasses/sendClass";
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

    /**
     * Получение фильтра для объекта друзья/запросы по пользователю и другу/запросу
     * @param user Значение сравниваемое с полем 'userID'
     * @param field Название поля по которому идет сравнение
     * @param friend Значение сравниваемое с полем название, которого передали в `field`
     * @returns {{comparisons: {user: {left: {type: string, value: string}, right: {type: string, value: *}, sign: string}, friend: {left: {type: string, value: *}, right: {type: string, value: *}, sign: string}}, tree: {and: string[]}}}
     * @private
     */
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

    /**
     * Получение объекта друга/запроса
     * @param project
     * @param object Название объекта
     * @param field Название поля по которому фильтруется объект
     * @param user Пользователь чей объект
     * @param friend Пользователь - друг/запрос в друзья
     * @returns {*}
     * @private
     */
    __checkFriend(project, object, field, user, friend){
        return sender.send({
            object: `${project}.${object}`,
            method: "get",
            parameters: {
                filter: this.__getFilterForFriend(user, field, friend)
            }
        });
    }

    /**
     * Создание отправленного запроса
     * @param project
     * @param user Пользователь, который отправил запрос
     * @param friend Пользователь, которому предназначен запрос
     * @returns {*}
     * @private
     */
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

    /**
     * Создание принятого запроса в друзья
     * @param project
     * @param user Пользователь, которому запрос пришел
     * @param friend Пользователь от которого пришел запрос
     * @returns {*}
     * @private
     */
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

    /**
     * Создание связи(дружбы) между пользователями
     * @param project
     * @param user
     * @param friend
     * @returns {*}
     * @private
     */
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

    /**
     * Удаление запроса в друзья
     * @param project
     * @param user
     * @param field Название поля (принятый/отправленный запрос)
     * @param friend
     * @returns {*}
     * @private
     */
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
