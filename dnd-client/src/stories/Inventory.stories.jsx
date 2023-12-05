import { InventoryContainer } from "../components";

export default {
    title: "Components/Inventory",
    component : InventoryContainer
}

const Template = args => <InventoryContainer {...args} />

export const inventory1 = Template.bind()
inventory1.args = {
    gold : 69,
    gems : 420,
    crystals : 720
}

export const inventory2 = Template.bind()
inventory2.args = {
    gold : 0,
    gems : 0,
    crystals : 0
 }

 export const inventory3 = Template.bind()
 inventory3.args = {
    gold : 999999,
    gems : 999999,
    crystals : 999999
 }