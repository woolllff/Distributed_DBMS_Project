import React, { Component } from 'react';
import {
    FormControl,
    FormLabel,
    FormErrorMessage,
    FormHelperText,
    Stack,
    Box,
    Center,
    Select
} from '@chakra-ui/react'
import { Button } from '@chakra-ui/react'
import { Input } from '@chakra-ui/react'
import axios from 'axios';

const backend_url = process.env.REACT_APP_BACKEND_URL


export default class GlobalSchemaRemover extends Component {

    constructor(props) {
        super(props)
        this.state = {
            id: "",
            avalableGS: []
        };

        this.getavalableGS()
        // console.log(this.avalableGS)

        this.handleSubmit = this.handleSubmit.bind(this)
    }

    getavalableGS() {
        axios({
            method: 'GET',
            headers: { 'content-type': 'application/json' },
            url : backend_url + "/mainApp/GlobalSchema",
            // url: "http://localhost:8000/mainApp/GlobalSchema",
        }).then((res) => {

            // console.log(res)
            var prevState = this.state;
            for (let i = 0; i < res.data.length; i++) {
                let l = res.data[i]["id"];
                // console.log(l)
                prevState.avalableGS = [...prevState.avalableGS, l];
            }
            this.setState(prevState)
            // this.state = prevState

        });
    }

    updateID(e) {
        let prevState = this.state;
        prevState.id = e.target.value;
        this.setState(prevState);
    }


    handleSubmit(event) {
        console.log("submit called")
        event.preventDefault();
        // console.log(this.avalableGS)

        axios({
            method: 'DELETE',
            headers: { 'content-type': 'application/json' },
            data: JSON.stringify({
                "id": this.state.id
            }),
            url : backend_url + "/mainApp/GlobalSchema",
            // url: "http://localhost:8000/mainApp/GlobalSchema",
        }).then((res) => {
            console.log(res)
        });

    }


    render() {

        return (

            <Center>
                <FormControl onSubmit={this.handleSubmit} >



                    <Stack paddingLeft='20' direction={['column', 'row']} spacing='24px' >

                        <Box>
                            <Select placeholder='Global schema ID' name="globalSchema_id" onChange={e => this.updateID(e)}>
                                {this.state.avalableGS.map((val, i) => (
                                    <option key={i} value={val} >{val}</option>
                                ))}
                            </Select>
                        </Box>

                    </Stack>

                    <Box>
                        <Button colorScheme='blue' className="buttonSubmit" type="button" onClick={(e) => this.handleSubmit(e)}>Submit</Button>
                    </Box>

                </FormControl>

            </Center>
        );
    }
}

