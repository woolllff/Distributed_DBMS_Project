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
import { formToJSON } from 'axios';

const backend_url = process.env.REACT_APP_BACKEND_URL


export default class GlobalSchemaMaker extends Component {

    constructor(props) {
        super(props)
        this.state = {
            localSchemasAvalable :  [],
            schemaName: "",
            localSchemas: {"ids" : []}
        };

        this.getAvalableLS()


        this.handleSubmit = this.handleSubmit.bind(this)
    }

    getAvalableLS(){
        axios({
            method: 'GET',
            headers: { 'content-type': 'application/json' },
            url: backend_url + "/mainApp/LocalSchema" ,
            // url:   "http://localhost:8000/mainApp/LocalSchema",
        }).then((res) => {
            // console.log(res)
            var prevState = this.state;
            for(let i = 0; i < res.data.length; i++ )
            {
                let l = res.data[i]["id"];

                prevState.localSchemasAvalable = [ ... prevState.localSchemasAvalable, l ];
            }
            this.setState(prevState)
            // this.state = prevState
        });
    }

    updateSchameName(e) {
        let prevState = this.state;
        prevState.schemaName = e.target.value;
        this.setState(prevState);
    }

    updateLocalSchemas(e, index) {
        let prevState = this.state;
        prevState.localSchemas["ids"][index] = e.target.value;
        this.setState(prevState);
        console.log(this.state.localSchemas);
    }

    addlocalSchema(){
        let prevState = this.state;
        let l = prevState.localSchemas["ids"].push(prevState.localSchemas["ids"][-1]);
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
                "localSchemas": JSON.stringify(this.state.localSchemas)
            }),
            url: backend_url + "/mainApp/GlobalSchema",
            // url: "http://localhost:8000/mainApp/GlobalSchema",
        }).then((res) => {
            console.log(res)
        });

    }


    render() {

        return (

            <Center>
                <FormControl onSubmit={this.handleSubmit} >
                    <Box>
                        <FormLabel >GlobalSchema Name</FormLabel >
                        <Input type="text" name="dbName" value={this.state.schemaName || ""} onChange={e => this.updateSchameName(e)} />
                    </Box>

                   

                    {this.state.localSchemas["ids"].map((id, s_index) => (

                        <Stack paddingLeft='20' direction={['column', 'row']} spacing='24px' key={s_index}>

                            <Box>

                                <Select placeholder='Local schema ID' name="localSchema_id" onChange={e => this.updateLocalSchemas(e, s_index)}>
                                    {this.state.localSchemasAvalable.map((val,i) => (
                                        <option key = {i} value={val} >{val}</option>
                                    ))}
                                </Select>

                            </Box>

                        </Stack>
                    ))}

                    <Box>
                        <Button style={{ display: "flex", justifyContent: "center", alignItems: "center" }} colorScheme='blue' type="button" className="Add localSchema" onClick={() => this.addlocalSchema()}>Add Local Schema</Button>
                    </Box>

                    <Box>
                        <Button colorScheme='blue' className="buttonSubmit" type="button" onClick={(e) => this.handleSubmit(e)}>Submit</Button>
                    </Box>
                </FormControl>

            </Center>
        );
    }
}

