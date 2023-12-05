import React from "react";
import { PartyContainer } from "../components";

import Sprite1 from "../assets/images/sprite1.png"
import Sprite2 from "../assets/images/sprite2.png"
import Sprite3 from "../assets/images/sprite3.png"
import Sprite4 from "../assets/images/sprite4.png"
import Sprite5 from "../assets/images/sprite5.png"
import Sprite6 from "../assets/images/sprite6.png"
import Sprite7 from "../assets/images/sprite7.png"
import Sprite8 from "../assets/images/sprite8.png"
import Sprite9 from "../assets/images/sprite9.png" 

const spritesArray = [Sprite1, Sprite2, Sprite3, Sprite4, Sprite5, Sprite6, Sprite7, Sprite8, Sprite9]
export default {
    title: "Components/PartyContainer",
    component : PartyContainer
}

function convertImageToBase64(file, callback) {
    var reader = new FileReader();
    reader.onload = function(e) {
        callback(e.target.result);
    };
    reader.readAsDataURL(file);
}

const partyList = [
    {
        id: 1,
        name: "Aelar",
        level: 5,
        gameClass: "Wizard",
        MP: 150,
        HP: 80,
        STA: 70
    },
    {
        id: 2,
        name: "Brissa",
        level: 3,
        gameClass: "Archer",
        MP: 60,
        HP: 120,
        STA: 110
    },
    {
        id: 3,
        name: "Cassius",
        level: 4,
        gameClass: "Knight",
        MP: 40,
        HP: 150,
        STA: 90
    },
    {
        id: 4,
        name: "Daelen",
        level: 2,
        gameClass: "Rogue",
        MP: 80,
        HP: 100,
        STA: 120
    },
    {
        id: 5,
        name: "Eldeth",
        level: 6,
        gameClass: "Cleric",
        MP: 180,
        HP: 90,
        STA: 60
    },
    {
        id: 6,
        name: "Fenrir",
        level: 1,
        gameClass: "Barbarian",
        MP: 30,
        HP: 200,
        STA: 100
    },
    {
        id: 7,
        name: "Gwenn",
        level: 7,
        gameClass: "Sorcerer",
        MP: 200,
        HP: 70,
        STA: 50
    },
    {
        id: 8,
        name: "Horus",
        level: 8,
        gameClass: "Paladin",
        MP: 100,
        HP: 160,
        STA: 80
    },
    {
        id: 9,
        name: "Ivy",
        level: 9,
        gameClass: "Druid",
        MP: 220,
        HP: 60,
        STA: 40
    }
];



for (let i = 0; i < partyList.length; i++) {
    partyList[i].profile_picture = spritesArray[i]
}

const Template = args => <PartyContainer {...args} />

export const partyContainer1 = Template.bind();
partyContainer1.args = {
    partyList : partyList.slice(0, 6)
}

export const PartyContainer2 = Template.bind();
PartyContainer2.args = {
    partyList : partyList.slice(1, 3)
}

export const PartyContainer3 = Template.bind();
PartyContainer3.args = {
    partyList : partyList.slice(6,9)
} 

export const PartyContainer4 = Template.bind();
PartyContainer4.args = {
    partyList : partyList.slice(4,5)
}