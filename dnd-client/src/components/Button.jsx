import { cva } from "class-variance-authority"
import { cn } from '../../utils'
import React from "react"

const buttonVariant = cva(
    'inline-flex items-center justify-center rounded-md text-sm font-medium text-white font-custom',
    {
        variants : {
            variant : {
                primary_blue :
                    'transition bg-gradient-to-t from-blue-800 to-blue-500',
                secondary_brown : 
                    'transition bg-gradient-to-t from-red-800 to-red-500',
                inventory : 
                    'transition bg-gradient-to-t from-green-900 to-green-700',
            },
            size : {
                default : "h-8 py-2 px-4",
                sm : 'h-9 w-60 px-2',
                lg : "h-40 w-80 py-4 px-4"
            }
        },
        defaultVariants : {
            variant: 'primary_blue',
            size : 'default' 
        }
    }
)

const Button = ({className, size, variant, handleClick, ...props}) => {
    return (
        <button className={cn(buttonVariant({variant, size}), className)} onClick={handleClick} {...props} />
    )
}

export { Button, buttonVariant }