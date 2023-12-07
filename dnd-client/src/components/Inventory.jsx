import GoldImage from '../assets/images/gold-sprite.png'
import GemImage from '../assets/images/gem-sprite.png'
import CrystalImage from '../assets/images/crystal-sprite.png'
import InventoryImage from '../assets/images/inventory.png'
import { Button } from './Button'

export const InventoryContainer = (totalCurrency) => {
    const {gold, gems, crystals } = totalCurrency;
    return (
        <div className="font-custom flex flex-col items-center justify-evenly bg-slate-800 border border-red-950 w-80 text-white text-left rounded-md h-80">
            <div className='flex flex-col flex-auto content-around mt-2'>
                <div className="flex flex-row flex-auto my-3 h-1 justify-around">
                    <img className="h-12 w-12" src={GoldImage} alt="gold"/>
                    <div className="bg-slate-700 px-5 py-2 ml-2 h-fit w-48">Gold: { gold }</div>
                </div>
                <div className="flex flex-row flex-auto mb-3 h-1">
                    <img className="h-10 w-10 ml-1" src={GemImage} alt="gem"/>
                    <div className="bg-slate-700 px-5 py-2 ml-3 h-fit w-48">Gems: { gems }</div>
                </div>
                <div className="flex flex-row flex-auto mb-3 h-1">
                    <img className="h-12 w-12" src={CrystalImage} alt="crystal"/>
                    <div className="bg-slate-700 px-5 py-2 ml-2 h-fit w-48">Crystals: { crystals }</div>
                </div>
            </div>
            <Button className="my-5" size="sm" variant="inventory" handleClick={ () => "dummy function" }>
                <img src={InventoryImage} className="h-6 w-6 mr-4 text-left" alt="Inventory"/>
                Inventory
            </Button>    
        </div>
    )
}