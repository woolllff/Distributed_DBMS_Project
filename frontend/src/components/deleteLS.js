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


export default class LocalSchemaRemover extends Component {

    constructor(props) {
        super(props)
        this.state = {
            id: "",
            avalableLS: [],
        };

        this.getavalableLS();
        // console.log(this.avalableLS);

        this.handleSubmit = this.handleSubmit.bind(this)
    }

    getavalableLS() {
        axios({
            method: 'GET',
            headers: { 'content-type': 'application/json' },
            url: "http://localhost:8000/mainApp/LocalSchema",
        }).then((res) => {
            
            // console.log(res)
            var prevState = this.state;
            for (let i = 0; i < res.data.length; i++) {
                let l = res.data[i]["id"];

                prevState.avalableLS = [...prevState.avalableLS, l];
            }
            this.setState(prevState)
            // this.state = prevState;
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

        axios({
            method: 'DELETE',
            headers: { 'content-type': 'application/json' },
            data: JSON.stringify({
                "id": this.state.id
            }),
            url: "http://localhost:8000/mainApp/LocalSchema",
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

                            <Select placeholder='Local schema ID' name="localSchema_id" onChange={e => this.updateID(e)}>
                                {this.state.avalableLS.map((val, i) => (
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

