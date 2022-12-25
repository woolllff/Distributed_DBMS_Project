import React, { Component } from 'react';
import {
    FormControl,
    FormLabel,
    Box,
    Center,
} from '@chakra-ui/react'

import { Button } from '@chakra-ui/react'
import { Input } from '@chakra-ui/react'
import axios from 'axios';

const backend_url = process.env.REACT_APP_BACKEND_URL


export default class LocalSchemaMaker extends Component {

    constructor(props) {
        super(props)
        this.state = {
            dbName: "",
            serverIP: "",
            serverPort: "3306",
            serverUser: "",
            serverPass: "",
            schemaName: "",

        };

        this.localSchemasAvalable = []

        this.handleSubmit = this.handleSubmit.bind(this)
    }

    updateserverIP(e) {
        // console.log("update called")
        let prevState = this.state;
        prevState.serverIP = e.target.value;
        this.setState(prevState);
    }

    updateserverPort(e) {
        // console.log("update called")
        let prevState = this.state;
        prevState.serverPort = e.target.value;
        this.setState(prevState);
    }

    updateserverUser(e) {
        let prevState = this.state;
        prevState.serverUser = e.target.value;
        this.setState(prevState);
    }

    updateserverPass(e) {
        let prevState = this.state;
        prevState.serverPass = e.target.value;
        this.setState(prevState);
    }

    updatedbName(e) {
        let prevState = this.state;
        prevState.dbName = e.target.value;
        this.setState(prevState);
    }

    updateSchameName(e) {
        let prevState = this.state;
        prevState.schemaName = e.target.value;
        this.setState(prevState);
    }


    handleSubmit(event) {
        console.log("submit called")
        event.preventDefault();

        axios({
            method: 'POST',
            headers: { 'content-type': 'application/json' },
            data: JSON.stringify({
                "schemaName": this.state.schemaName,
                "serverIP": this.state.serverIP,
                "serverPort": this.state.serverPort,
                "serverUser": this.state.serverUser,
                "serverPass": this.state.serverPass,
                "dbName": this.state.dbName
            }),
            url : backend_url + "/mainApp/LocalSchema",
            // url: "http://localhost:8000/mainApp/LocalSchema",
        }).then((res) => {
            console.log(res)
        });
        

    }


    render() {

        return (

            <Center>
                <FormControl onSubmit={this.handleSubmit} >

                    <Box>
                        <FormLabel >LocalSchema Name</FormLabel >
                        <Input type="text" name="dbName" value={this.state.schemaName || ""} onChange={e => this.updateSchameName(e)} />
                    </Box>

                    <Box>
                        <FormLabel >Server Ip </FormLabel >
                        <Input type="text" name="serverIP" value={this.state.serverIP || ""} onChange={e => this.updateserverIP(e)} />
                    </Box>

                    <Box>
                        <FormLabel >Server Port </FormLabel >
                        <Input type="text" name="serverIP" value={this.state.serverPort || ""} onChange={e => this.updateserverPort(e)} />
                    </Box>

                    <Box>
                        <FormLabel >Server username</FormLabel >
                        <Input type="text" name="serverUser" value={this.state.serverUser || ""} onChange={e => this.updateserverUser(e)} />
                    </Box>

                    <Box>
                        <FormLabel >Server Password</FormLabel >
                        <Input type="text" name="serverPass" value={this.state.serverPass || ""} onChange={e => this.updateserverPass(e)} />
                    </Box>

                    <Box>
                        <FormLabel >Database name</FormLabel >
                        <Input type="text" name="dbName" value={this.state.dbName || ""} onChange={e => this.updatedbName(e)} />
                    </Box>

                    <Box>
                        <Button colorScheme='blue' className="buttonSubmit" type="button" onClick={(e) => this.handleSubmit(e)}>Submit</Button>
                    </Box>
                </FormControl>

            </Center>
        );
    }
}

