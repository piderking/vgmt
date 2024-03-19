import Image from "next/image";
import { Button } from "@/components/ui/button"
import Navbar from "@/components/ui/navbar";

// TODO: Add flex-inital and widths to text boxes

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
              <div className="flex-inital w-96">
                <h1 className="text-3xl font-medium text-text pb-4">VGMT</h1>
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
            <div className="flex-col flex flex-inital w-96 items-center text-center">
              <h2 className="text-2xl pl-0.5 text-text font-medium">Speed</h2>
              <p className="font-extralight text-text">Accurate* blood sugar predictions without the use of on body devices.</p>
            </div>
            <div className="flex-1"></div>
          </div>
          <div className="flex-1 flex-col flex items-center">
            <div className="flex-1 flex-row flex">
              <div className="flex-1"></div>
              <div className="flex-col flex flex-inital w-96 items-center text-center">
                <h2 className="text-2xl pl-0.5 text-text font-medium">Practice</h2>
                <p className="font-extralight text-text">Accurate* blood sugar predictions without the use of on body devices.</p>
              </div>
              <div className="flex-1"></div>
            </div> 
          </div>
        </div>
        <div className="bg-swight h-64 flex-col flex pt-20">
          <div className="flex-1 text-center pb-16">
            <h2 className="text-3xl pl-0.5 text-text font-medium">Predictive Solutions</h2>
          </div>
          <div className="flex-1"></div>
          <div className="flex-4 flex flex-row text-center">
            <div className="flex-1"></div>
            <div className="flex-4">
              
              <h2 className="text-xl pb-2 text-text font-medium">Global</h2>
              <p className="font-extralight text-text pb-6">Instant quick start opportunity to for a series of blood sugar prediction based on only a few* manual fingersticks a day.</p>
              <Button variant={"link"} className="bg-button text-textbutton w-32 font-light">Learn More</Button>
            </div>
            <div className="flex-1"></div>
            <div className="flex-1"></div>
            <div className="flex-4">
              <h2 className="text-xl pb-2 text-text font-medium">Personal</h2>
              <p className="font-extralight text-text pb-6">A personalized and more accurate blood sugar reading  prediction matrix with a low amount of fingersticks daily!</p>
              <Button variant={"link"} className="bg-button text-textbutton w-32 font-light">Learn More</Button>

            </div> 
            <div className="flex-1"></div>
          </div>
        </div>
        <div className="h-16 bg-swight text-center">
          
        </div>
        <div className="bg-swight h-70 pt-32 flex flex-row text-center pb-6 ">
          <div className="flex-1"></div>
          <div className="flex-5 flex-col flex">
            <div className="flex-1">
            <h2 className="text-3xl pl-0.5 text-text font-medium pb-12">Timeline</h2>
            </div>
            <div className="flex-3 ht-12 border-[#739CBF] border-2 flex flex-row">
              <div className="flex-2 bg-[#739CBF]">
                <p className="invisible">ds</p>
              </div>
              <div className="flex-3"></div>
              <div className="flex-1"></div>
              <div className="flex-1"></div>
              <div className="flex-1"></div>
              <div className="flex-1"></div>
            
            </div>
            <div className="flex-4">
              <div className="pt-16 flex  text-right  flex-row">
                <div className="flex-1 text-l pr-12 text-text rotate-[315deg]">Development</div>
                <div className="flex-1 text-l pr-12 text-text rotate-[315deg]">Development</div>
                <div className="flex-1 text-l pr-12 text-text rotate-[315deg]">Development</div>
                <div className="flex-1 text-l pr-12 text-text rotate-[315deg]">Development</div>
                <div className="flex-1 text-l pr-12 text-text rotate-[315deg]">Development</div>
              </div>
            </div>
          </div>
          <div className="flex-1"></div>
          
        </div>
        <div className="bg-swight h-96 flex-col flex pt-24">
          <div className="flex-1 text-center">
            <h2 className="text-3xl pl-0.5 text-text font-medium">Development</h2>
            
          </div>
          <div className="flex-1"></div>
          <div className="flex-4 flex flex-row text-center">
            <div className="flex-1"></div>
            <div className="flex-4">
              
              <h2 className="text-xl pb-2 text-text font-medium">Collection</h2>
              <p className="font-extralight text-text pb-6">Data collection piloting programs have been launched in order to collect enough data to train a strong global model. Click to learn more about partnering with VGM to earn rewards. </p>
              <Button variant={"link"} className="bg-button text-textbutton w-32 font-light">Partner Up!</Button>
            </div>
            <div className="flex-1"></div>
            <div className="flex-1"></div>
            <div className="flex-4">
              <h2 className="text-xl pb-2 text-text font-medium">Training</h2>
              <p className="font-extralight text-text pb-6">In order to build a strong foundational AI, extensive researching on a new structured neural network to make accurate predictions* that can be used for patients without confusion on factors like age, gender, activity levels, weights and previous history.</p>
              <Button variant={"link"} className="bg-button text-textbutton w-32 font-light">Learn More</Button>

            </div> 
            <div className="flex-1"></div>
          </div>
        </div>
        <div className="bg-swight h-96 flex-col flex pt-20">
          <div className="flex-1 text-center">
            <h2 className="text-3xl pl-0.5 text-text font-medium">Funding</h2>
            
          </div>
          <div className="flex-1"></div>
          <div className="flex-4 flex flex-row text-center">
            <div className="flex-2"></div>
            <div className="flex-4">
              <p className="font-extralight text-text pb-6">Funding must be secured in order to obtain resources to train and host large neural networks and web servers. As well as funding our massive accessible data storage** incentive. To inquire more about funding , click funding page</p>
              <Button variant={"link"} className="bg-button text-textbutton w-32 font-light">Learn More</Button>

            </div> 
            <div className="flex-2"></div>
          </div>
        </div>
      </div>

    </main>
  );
}
