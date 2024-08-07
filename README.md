# Solar axion detection with SABRE-South
Taaseen Islam, Laby Vacation Scholar at UniMelb Winter 2024. Feel free to email me at u7121940@anu.edu.au for any questions (or my personal email taaseen.islam13@gmail.com after I graduate in late 2025).  
## Important/useful papers:
- "Bragg-Primakoff Axion Photoconversion in Crystal Detectors", Dent et.al 2023 http://arxiv.org/abs/2307.04861
    - Describes the ultimate equation, process, and exclusion plot to work towards. Note that many of the derivations assume monatomic crystals, so some extra steps are involved with NaI (which I will attempt to describe)
- "On Coherence in Bragg-Primakoff Axion Photoconversion", Thompson 2023 http://arxiv.org/abs/2309.01767
    - A PhD thesis with the work discussed in Dent et.al. Has several other useful results, but is obviously much longer.
- "The landscape of QCD axion models", Di Luzio et.al 2020 https://arxiv.org/abs/2003.01100v4
    - Describes axions and their representations with various models for a more theoretical description of what's happening
- "Prospects of solar axion searches with crystal detectors" Cebrian et.al 1999 http://arxiv.org/abs/astro-ph/9811359
    - Older look at using crystals to detect axions with more thorough derivations that do differ from Dent et.al's results (mainly from the definitions of some parameters)
## Code and problem description
This code was developed by me over 4 weeks with the ultimate goal of evaluating SABRE-South's prospects in finding solar axions. It calculates the event rate as derived by Dent et.al and integrates this absorption rate over time (incorporating changing solar position) to get an initial exclusion region assuming zero background. 

To incorporate background, I used simple Poisson statistics ($\mu=N_{bg}$, $\sigma=\sqrt{N_{bg}}$, require $N_{obs} = N_{bg}+N_{ax} > 1.96\sqrt{N_{obs}}$ for significance assuming $N_{bg}>>N_{ax}$) Assuming an $N_{bg}$ from a background rate constant over energy but variable over time. This increases the maximum required events $N_{ax}$ for significance, which would increase the value of a coupling constant that would result in this many detections.

To include absorption, I assumed that absorption multiplies a constant ($<1$) on the no-absorption event rate. The event rate is simply proportional to $g_{a\gamma}^4$, meaning absorption also just multiplies the required coupling constant by a fixed amount. This constant was determined from Thompson's PhD thesis comparing their model of SABRE with and without absorption to obtain this constant.

Background and absorption are the two main improvements that can be made onto results. Notably, the background level might actually be higher than what I estimated--since the peaks of the background and axion spectrum match--and absorption will in theory be more significant than what I estimated--since absorption is more impactful for fewer larger crystals than several smaller crystals and Thompson used the latter ($25\times 2$ kg crystals instead of what SABRE really has). This means that unfortunately SABRE's axion performance might actually be even weaker than what I estimated.

## Directories
Notebooks is the main folder for the analysis. Everything should work with no major issues, and I've tried to make sure everything here makes sense. These notebooks will make the most sense if you follow them in the order:
- math_notes (look here for form/structure factors!)
- compute_dndt (and axion_functions)
- solar_path
- time_integrate
- energy_spectrum (unrelated but axion detection has a very interesting many-peaked cspectrum)
- result_plots
    - This is the last notebook that I'd say is pretty complete. Everything from here is largely incomplete so imporvements can be made.
- background
- absorption_incomplete

I've put my final poster in the "results" directory with the plots I made for the poster. These plots should be easy to replicate in the main notebooks directory, but their creation is also documented in Deprecated...

Deprecated is full of the notebooks I initially created while working on this project. Most of these will not work without running cells in weird orders and adding new stuff and will also make very little sense, but I've kept it here just in case something here _might_ work. I would not recommend looking through here if there's a problem you want to solve--it will probably be easier to figure out a solution yourself than deciphering the evil Necronomicon banished to this folder. 