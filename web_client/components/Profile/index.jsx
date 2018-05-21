import React, { Component } from 'react'
import { Link } from 'react-router-dom'
import axios from 'axios'

class Profile extends Component {
    constructor(props) {
        super(props);

        this.state = {
            user: []
        };
    }


    componentWillMount() {
        axios.get(`/users/adm/`).then(response => {
            this.setState({user: response.data})
        })
    }

    render() {
        return(
            <div id="profile" className="mx-2 my-2 bg-dark text-center py-1">
                <div className="row justify-content-center">
                    <div className="col">
                    </div>
                    <div className="col">
                        <img width="150px" src={this.state.user.avatar} id="avatar"  className="rounded-circle img-responsive border border-secondary m-2" alt=""/>
                    </div>
                    <div className="col">
                        <a type="button" className="add-button text-light float-right px-1" data-toggle="modal" data-target="#editUser" href="#editUser" ><span className="oi oi-pencil"/>edit</a>
                    </div>
                </div>

                <h2 id="username">{ this.state.user.username }</h2>
                <h3 id="first_name">{ this.state.user.first_name }</h3>
                <h3 id="lastname"> { this.state.user.last_name }</h3>
                <p id="about"><strong>About: </strong>{ this.state.user.info }</p>
                <p id="birthdate"><strong>Birthdate: </strong>{ this.state.user.date_of_birth }</p>
            </div>
        )
    }
}


export default Profile;
