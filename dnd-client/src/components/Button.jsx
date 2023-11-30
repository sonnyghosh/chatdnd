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
                    'transition bg-gradient-to-t from-red-800 to-red-500',
            },
            size : {
                default : "h-10 py-2 px-4",
                sm : 'h-9 px-2',
                lg : "h-11 py-4 px-4"
            }
        },
        defaultVariants : {
            variant: 'primary_blue',
            size : 'default' 
        }
    }
)

const Button = ({className, size, variant, ...props}) => {
    return (
        <button className={cn(buttonVariant({variant, size}), className)} {...props} />
    )
}

export { Button, buttonVariant }