import React from 'react'
import '../App.css'

function TextBlockBot(args) {

    return (
        <div className="textuser-div">
            <div className='textblockuser'>
                {/* this is a comment */}
                <p>{args.val}</p>
            </div>
        </div>
    )
}

export default TextBlockBot
