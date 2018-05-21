import React, { Component } from 'react'
import { BrowserRouter as Router, Route, IndexRoute, Link } from 'react-router-dom'
import {default as Profile} from '../Profile'


class App extends Component {
    render(){
        return(
            <Router>
                <Route path="/" component={ Profile }>
                </Route>
            </Router>
        );
    }
}


export default App
