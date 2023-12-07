import React, {useState, useEffect} from "react";

export const StoryContainer = () => {
    const storyRequest = {
        newPrompt : "Seizing the opportunity presented by the weakened state of the Crystal Behemoth, you decide to press the attack with your double-handed axe. Closing the distance between you and the creature, you target the areas where the crystalline surface has been chipped away by the fireballs."
    }
    const { newPrompt } = storyRequest;

    return (
        <div className="ml-auto mr-auto w-2/3 h-80 p-2 font-custom bg-slate-800 text-white border border-red-900" >
            <p>{ newPrompt }</p> 
        </div>
    )
}