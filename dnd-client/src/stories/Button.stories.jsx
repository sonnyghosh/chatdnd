import React from 'react'
import { Button } from '../components/Button'

export default {
    title: "Components/Button",
    component : Button,
    argTypes : { handleClick : { action : "handleClick" } }
}

const Template = args => <Button {...args} />

export const storyOption1 = Template.bind({})
storyOption1.args = {
    size:'lg',
    variant:'primary_blue',
    label:'option1',
    children : 'Deliver a final powerful blow with your double-handed axe to defeat the Crystal Behemoth.',
}

export const storyOption2 = Template.bind({})
storyOption2.args = {
    size:'lg',
    variant:'primary_blue',
    label:'option2',
    children: "Retreat temporarily to assess the situation and plan the next move."
}

export const storyOption3 = Template.bind({})
storyOption3.args  = {
    size:'lg',
    variant:'primary_blue',
    label:"option3",
    children:'Conjure a protective barrier using your Phoenix Feather Quill to shield yourself from any potential counterattack.'
}

export const egress1 = Template.bind({})
egress1.args = {
    size:'sm',
    variant:'primary_blue',
    label:"egress1",
    children:'Keep Exploring'
}

export const egress2 = Template.bind({})
egress2.args  = {
    size:'sm',
    variant:'primary_blue',
    label:"egress2",
    children:'Shop'
}

// export const inventory = Template.bind({})
// inventory.args = {
//     size:'sm',
//     variant:'inventory',
//     children:'Inventory',
// }

export const startAdventure = Template.bind({})
startAdventure.args = {
    size:'sm',
    variant:'secondary_brown',
    label:"startAdventure",
    children:'Start Adventure'
}
