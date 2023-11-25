import React, {useState, useEffect} from "react";
import { findRenderedComponentWithType } from "react-dom/test-utils";

function Navbar() {
   return (
    <div className="flex flex-row flex-auto border-b-2 border-red-400">
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
        <div className="flex flex-col w-1/2">
            <div className="border-l-2 border-b-2 border-red-400 flex flex-row flex-auto">
                <p>ATK : {ATK}</p>
                <p>DEF : {DEF}</p>
                <p>CHA : {CHA}</p>
                <p>ATK : {INT}</p> 
                <p>WIS : {WIS}</p>
            </div>
            <div className="border-l-2 border-b2 border-red-400 flex flex-row flex-auto">
                <p>Level : { level }</p>
                <p>HP : { HP }</p>
                <p>MP : { MP }</p>
                <p>STA : { STA } </p>
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
        <div className="flex flex-col flex-auto border-l-2 border-b-2 border-red-400">
            <p>Name : {name} </p>
            <p>Weapon : {weapon}</p>
            <p>Class : {playerClass} </p>
        </div>
    )
}

function DieRollContainer() {
    const dieRoll = {
        currentRoll : 20,
        rollNeeded : 30,
        modifiers : 4
    }

    return (
        <>
        </>
    )
}

export {Navbar} from "Navbar";