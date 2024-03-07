import Image from 'next/image'

export default function Navbar(){


    return (
        <div className="flex-initial flex flex-col min-h-1">
            <div className="flex h-12 flex-none flex-row text-center">
            <div className="flex-1 h-12 flex flex-col text-center">
                <div className="flex-1"></div>
                <div className="flex-1 flex flex-row " >
                <div className="flex-2"></div>
                <div className="flex-3 object-fill">
                    <div className=' w-12 pt-1 absoulute'>
                    <Image src="/logo.png"
                        width={256}
                        height={256}
                        alt="lOGO" 
                        objectFit="cover"
                    />
                    </div>
                   
                </div>
                <div className="flex-2 pl-2 text-left">
                    <h1 className="text-xl pl-0.5">VGMT</h1>
                </div>
                <div className="flex-4"></div>
                
                </div>
                <div className="flex-2"></div>
            </div>
            
            <div className="flex-3  flex flex-col">
                <div className='flex-1'></div>
                <div className='flex-1 flex flex-row text-text'>
                    <div className="flex-1"></div>
                    <div className="flex-2">ABOUT</div>
                    <div className="flex-2">PRODUCTS</div>
                    <div className="flex-2">CONTACT</div>
                    <div className="flex-2">HUB</div>
                    <div className="flex-1"></div>
                    </div>
                <div className='flex-1'></div>
            </div>
            <div className="flex-1"></div>
            </div>
            <div className="bg-line h-[1px] flex-none"></div>
              
        </div>
    )
}