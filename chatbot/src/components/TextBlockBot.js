import React from 'react'
import '../App.css'

function TextBlockBot(args) {

    return (
        <div className="textbot-div">
            <div className='textblockbot'>
                <p>{args.val}</p>
            </div>
        </div>
    )
}

export default TextBlockBot
