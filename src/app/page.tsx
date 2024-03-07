import Image from "next/image";
import { Button } from "@/components/ui/button"
import Navbar from "@/components/ui/navbar";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col font-karla">
      <Navbar />
      <div className="flex-auto pt-16">
        <div className="h-96 flex flex-row">
          <div className="flex-1"></div>
          <div className="flex-2 flex flex-col">
            
            <div className="flex-3 text-center flex flex-col">
              <div className="flex-1"></div>
              <div className="flex-5">
                <h1 className="text-3xl font-medium text-text">VGMT</h1>
                <p className="font-extralight text-text">Accurate* blood sugar predictions without the use of on body devices.</p>
                <div className="pt-10 flex flex-row">
                  <div className="flex-3">
                    <Button variant={"link"} className="bg-button text-textbutton w-32 font-light">Learn More</Button>
                  </div>
                  <div className="flex-1"></div>
                  <div className="flex-3">
                  <Button variant={"outline"} className="bg-transparent outline-[#2F4963] text-text outline-2 w-32 font-light">Pros & Cons</Button>
                  </div>
                </div>
              </div>
              <div className="flex-1"></div>
              
              
            </div>
            <div className="flex-1"></div>
            
          </div>
          <div className="flex-1"></div>
          <div className="flex-2 flex-col flex">
            
            <Image className="object-fill
             flex-1 h-96 w-72" src="/phone.png"
                          width={550}
                          height={500.72}
                          alt="lOGO" 
                          
                      />
              
          <div className="flex-1"></div>
              
          </div>
          <div className="flex-1"></div>
        </div>
      <div className="bg-swight h-64 flex-row flex pt-20">
          <div className="flex-1 flex-row flex">
            <div className="flex-1"></div>
            <div className="flex-col flex flex-4 items-center text-center">
              <h2 className="text-2xl pl-0.5 text-text font-medium">Speed</h2>
              <p className="font-extralight text-text">Accurate* blood sugar predictions without the use of on body devices.</p>
            </div>
            <div className="flex-1"></div>
          </div>
          <div className="flex-1 flex-col flex items-center">
            <div className="flex-1 flex-row flex">
              <div className="flex-1"></div>
              <div className="flex-col flex flex-4 items-center text-center">
                <h2 className="text-2xl pl-0.5 text-text font-medium">Practice</h2>
                <p className="font-extralight text-text">Accurate* blood sugar predictions without the use of on body devices.</p>
              </div>
              <div className="flex-1"></div>
            </div> 
          </div>
        </div>
        <div className="bg-swight h-96 flex-col flex pt-20">
          <div className="flex-1 text-center">
            <h2 className="text-2xl pl-0.5 text-text font-medium">Prediction Solutions</h2>
          </div>
        </div>
      </div>

    </main>
  );
}
