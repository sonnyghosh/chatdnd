import React, {useState, useEffect} from "react";
// import './output.css';

export const Navbar = () => {
   return (
    <div className="flex flex-row flex-auto border-b-2 border-red-400 text-sm bg-black text-white h-fit font-custom">
        {/* <SpriteContainer /> */}
        <InformationContainer />
        <DieRollContainer />
        <AttributesContainer />
    </div>
    )
}

function AttributesContainer() {
    const characterAttributes = {
        ATK : 30,
        DEF : 20,
        CHA : 30,
        INT : 30,
        WIS : 30,
        level : 4,
        HP : 100,
        MP : 100,
        STA : 100,
   }
   const {ATK, DEF, CHA, INT, WIS, level, HP, MP, STA} = characterAttributes;
    return (
        <div className="flex flex-col w-1/3">
            <div className="border-l-2 border-b-2 border-red-400 flex flex-row flex-auto justify-around">
                <p className="mt-1">ATK: {ATK}</p>
                <p className="mt-1">DEF: {DEF}</p>
                <p className="mt-1">CHA: {CHA}</p>
                <p className="mt-1">INT: {INT}</p> 
                <p className="mt-1">WIS: {WIS}</p>
            </div>
            <div className="border-l-2 border-red-400 flex flex-row flex-auto justify-around">
                <p className="mt-1">Level: { level }</p>
                <p className="mt-1">HP: { HP }</p>
                <p className="mt-1">MP: { MP }</p>
                <p className="mt-1">STA: { STA } </p>
            </div>
        </div>
   )
}

function InformationContainer() {
    const characterInfo = {
        name: "Luke Tyson",
        weapon: "Spear of Lightning",
        playerClass : "Bard",
    }
    const { name, weapon, playerClass } = characterInfo;
    return (
        <div className="flex flex-col flex-auto w-1/3 h-fit">
            <p className="ml-2">Name: {name} </p>
            <p className="ml-2">Weapon: {weapon}</p>
            <p className="ml-2 mt-1">Class: {playerClass} </p>
        </div>
    )
}

function DieRollContainer() {
    const dieRoll = {
        currentRoll : 20,
        rollNeeded : 30,
        modifiers : 4
    }
    const {currentRoll, rollNeeded, modifiers } = dieRoll;

    return (
        <div className="flex flex-col flex-auto border-l-2 border-red-400 w-1/6">
            <p className="ml-2">Current Roll: { currentRoll }</p>
            <p className="ml-2">Roll Needed: { rollNeeded }</p>
            <p className="ml-2 mt-1">Modifier: { modifiers }</p>
        </div>        
    )
}

// function SpriteContainer() {
//     const SpriteResponse = {
//         sprite_url : "main_character.png"
//     }
//     const { sprite_url } = SpriteResponse;

//     return (
//         <div className="w-1/6">
//             <img src={ sprite_url }/>
//         </div>
//     )
// }
