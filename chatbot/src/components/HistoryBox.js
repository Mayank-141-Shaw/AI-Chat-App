import React, { Component, useEffect, useState } from 'react'
//import RNFS from 'react-native-fs'
import TextBlockBot from './TextBlockBot'
import TextBlockUser from './TextBlockUser'
import submit_btn from '../Images/submit_btn.png'

import 'axios';


import '../App.css'
import axios, { Axios } from 'axios';

const botpath = '/Files/bot.txt'
const userpath = '/Files/user.txt'

// current text input given by user
var chatText = "";

// default message
const defMsg = "Hello! How can I help you?";

class HistoryBox extends React.Component{

    constructor(props){
        super(props)
        this.state = { 
            chatHistory : [],
        };
    }

    
    // read the files
    async readfileBot(path){
        //abort control
        const controller = new AbortController()
        const { signal } = controller
        let tempdata = []

        const botPattern = new RegExp(/(bot\.txt)$/i)
        const userPattern = new RegExp(/(user\.txt)$/i)

        if(botPattern.test(path)){
            await fetch(path, {mode: 'no-cors', signal: signal})
                .then(res => res.text()
                .then(data => {
                    // save data in databot list
                    tempdata = data.trim().split('\r\n')
                    console.log('got data')
                    console.log(tempdata)
                }))
                .catch(err => console.error(err))
            
            //controller.abort()
        }
        else if(userPattern.test(path)){
            await fetch(path, {mode: 'no-cors', signal: signal})
                .then(res => res.text()
                .then(data => {
                    // save data in userbot list
                    tempdata = data.trim().split('\r\n')
                    console.log('got data')
                    console.log(tempdata)
                }))
                .catch(err => console.error(err))

                //controller.abort()
        }
        else{
            console.log("Not matching any")
            return []
        }
        return tempdata
    }

    // function to format data in chatHistory
    putInChathistory(databot, datauser){
        var temp = []
        let ct = 0
        console.log('Inside here : '+databot+' || '+datauser)
        for(let id = 0; id<databot.length; id++){            
            temp.push(
                <TextBlockBot key={ct++} val={databot[id]}/>
            )
            temp.push(
                <TextBlockUser key={ct++} val={datauser[id]}/>
            )
        }
        return [...temp]
    }

    // the very beginning of the booting of the app when there is no data
    initializeChatHistory = () => {
        var temp = []
        let ct = 0
        temp.push( <TextBlockBot key={ct++} val={defMsg}/> )
        this.setState({
            chatHistory: temp,
        });
    }

    // get Data from files
    async getData(botpath, userpath){
        console.log('is inside getdata')
        var botdata = await this.readfileBot(botpath)
        console.log(botdata)
        var userdata = await this.readfileBot(userpath)
        console.log(userdata)
        var ch = this.putInChathistory(botdata, userdata)
        
        this.setState({
            chatHistory: [...ch],
        })
        console.log('ch : '+this.state.chatHistory)
    }

    // whever we type on a text input
    onTextInput = (e) => {
        chatText = e.target.value;
    }

    // auto scroll to bottom of chatbox
    scrollToBottom = () => {
        var scroll = document.getElementById('history-box-background');
        var xH = scroll.scrollHeight;
        scroll.scrollTo(0, xH);
    }


    async getResponse(req){
        let ml_service_url = 'localhost:9806/predict'
        let response = ''

        await axios.post(ml_service_url, JSON.parse(`{'input':${req}}`))
            .then((data) => {
                response = data['response']
            }, (error) => {
                console.log('Returning response error : '+error)
                response = 'Some error in getting response'
            });
            
        return response
    }


    // on clicking the submit button
    onButtonClick(){
        console.log(chatText)
        // here we will send the chatText to our model and receive response
        // which we will give as output for bot response

        // printing the request
        let len = this.state.chatHistory.length
        this.setState({
            chatHistory: [...this.state.chatHistory, <TextBlockUser key={len++} val={chatText} />]
        })
        this.scrollToBottom();


        // so print request and then the response

        setTimeout(() => {
            // getting response
            var res = this.getResponse(chatText)      // <------- insert model from here

            // printing the response
            let len = this.state.chatHistory.length
            this.setState({
                chatHistory: [...this.state.chatHistory, <TextBlockBot key={len++} val={res} />]
            })
        } , 100)

        this.scrollToBottom();

        // send this text to user.txt
        
    }

    // before the component is rendered
    componentWillMount(){
        console.log('is mounting')
        //this.getData(botpath, userpath)
    }                                                                                   

    // after the component is rendered
    componentDidMount(){                                    
        //console.log('tsd : '+this.state.databot)
        console.log('is mounted')
        this.initializeChatHistory()
        //this.loadModel()
        //this.getData(botpath, userpath)
        this.scrollToBottom();
    }

    // after the component is updates
    componentDidUpdate(){
        console.log('Updated')
        // auto scrollling the scroll box to the bottom
        this.scrollToBottom();
    }

    render(){
        return(
            <div>
            <div className="history-box-background" id="history-box-background">
                { this.state.chatHistory==null ? console.log('Empty Chat History') : this.state.chatHistory }
            </div>
            <div className="input-box-background">
            <input onChange={this.onTextInput} id='user-chat' type='text' className="text-input" placeholder='Enter your message here'/>
            <button onClick={this.onButtonClick} className="input-btn">
                <img src={submit_btn} alt='Submit'/>
            </button>
            </div>
            </div>
        )
        
    }
}

export default HistoryBox;