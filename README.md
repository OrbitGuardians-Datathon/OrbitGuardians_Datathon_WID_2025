# Orbit Guardians
# Women in Data Hackathon - SpaceAware

# We are **ORBIT GUARDIANS**
![Orbit Guardians](https://github.com/mygoal-javadeveloper/Orbit-Guardians/blob/main/OrbitGuardians_WID.png)

![I'm Competing](https://github.com/mygoal-javadeveloper/Orbit-Guardians/blob/main/I%E2%80%99m%20Competing!.png)



# **A SaaS Based International Space Traffic Management System**


Space is becoming increasingly more crowded.  In the last 60 years nearly 8,500 objects have been launched to space, about 1,500 in geosynchronous Earth orbit (GEO) and about 7,000 in low Earth orbit (LEO) (McDowell 2018). A large fraction remains especially in LEO. Going forward, LEO is expected to become more crowded. The concern is not just the increasing number of satellites and active payloads, but the amount of debris (rocket bodies, other inert bodies, dead payloads) in Earth’s orbit, which comprises more than 95 percent of the currently tracked objects in space. The U.S. Department of Defense (DoD) is currently tracking over 23,000 objects larger than 10 cm in diameter in Earth orbit (of these, almost 16,000 are in LEO, of which nearly 13,000 were classified as space debris). An estimated 500,000 objects larger than 1 cm in diameter are not currently tracked, and over 100 million objects smaller than 1 mm in diameter are likely not trackable (NASA Orbital Debris Program Office, year?).


It is not just the number of satellites that is increasing—the number of satellite operators has been increasing steadily over the last 60 years. More countries have become active in space. Smaller, lighter, and more capable satellites make Earth observation and remote sensing within the reach, not just of countries, but also corporations and individuals. For example, Bank Rakyat in Indonesia launched satellite BRIsat in 2016, built by Space System/Loral and launched by Arianespace, to manage its 50 million accounts. Another example is the CubeSat satellite launched by NanoRacks in 2019 under the auspices of Zac Manchester who was able to afford it through crowdfunding. This trend is likely to continue, making the space environment increasingly more crowded.


Although relatively few catastrophic collisions have occurred thus far in space, the likelihood of a collision is predicted to increase in the near future, given the expected growing number of objects in both LEO and GEO and limited ability to track objects’ orbits, which will make it difficult for operators to adequately avoid threats. This problem may be exacerbated if any of the proposed constellations of small satellites in LEO are launched, as they will dramatically increase the number of objects that require tracking, thus increasing the tracking and computational requirements for SSA in general, and conjunction warnings in particular.


Given that the systems developed to track space objects were developed at a time when there were fewer objects in space, the accuracy of prediction is low. Oftentimes, a DoD conjunction warning message has an error ellipse of 100 km or more [need citation]; and the rate of false positives is high as well [need citation]. Because of these two factors, as traffic in space grows, both the number of conjunction warning messages, as well as the rates of both false positives—and false negatives— are likely to increase.


As space capabilities become integral to more applications (e.g., earth observation, communications, global positioning), a growing number of countries are recognizing the security and economic value of space, and consequently, increasing their spending in space. The number of countries involved in space continues to increase.  A decade ago, fewer than 50 countries were investing in space.  Today, there are 70 [need citation].  In the coming decade, that number is expected to increase to more than 80 countries [need citation].


Many stakeholders indicated that they need to have trust and confidence in the data being shared for collision warnings and other SSA products [need citation].  Many acknowledged the usefulness of verifying the information that is part of any database[need citation]. There are many concerns with the current systems for provision of SSA. Some operators question the accuracy and especially the completeness of the information provided to them by the DoD [need citation]. For example, some South Korean government officials estimate that their country receives data on only about 40 percent of the objects tracked by the DoD, due to sensitivity of U.S. assets [need citation]. This distrust is further complicated by the lack of transparency related to computing outcomes such as probabilities of collision [need citation]. Owners and operators believe they require more information of high enough quality to make well-informed decisions about maneuvering. But because they do not know the process by which U.S.-provided information on an object’s location is processed into a collision assessment or warning, they often do not feel confident maneuvering based on that warning [need citation].


Given the countries’ dependence on space for critical national needs and societally critical endeavors, SSA is becoming important enough that most countries active in space activities want to establish SSA systems that are more independent in tracking objects in space [need citation].


Some nations are looking to decrease their dependence on the U.S. SSA system due to concerns that it might be the target of an adversarial attack [need citation]. Other stakeholders felt such an attack is unlikely, given the global nature of SSA and the widespread reliance on the U.S. system. Some (e.g., France) seek to be self-sufficient for reasons of national pride and sovereignty [need citation]. Others see it as a means by which to provide leadership in the domain and collaborate with 23 other nations [need citation]. Many countries that are pursuing their own SSA systems, explicitly intend to keep their systems interoperable with others internationally (e.g., Australia, Canada, Japan, United Kingdom) [need citation].

# Our Project Concept: An International STM SaaS Platform


As the number of satellites and debris in orbit continues to grow, no single country can track and manage space traffic effectively on its own. A SaaS-based Space Traffic Management (STM) platform offers a mechanism where countries can voluntarily contribute orbital and object data to a global system, but do so in a way that protects their independence and national priorities. By using standardized formats such as TLEs (Two-Line Elements), OMMs (Orbit Mean Elements Messages), and CDMs (Conjunction Data Messages), each nation can share only the subset of its data that is approved for publication. This ensures that sensitive or classified information remains under national control while still allowing the broader international community to benefit from a more transparent, aggregated picture of orbital activity.


For participating countries, interoperability is achieved by adhering to agreed-upon international data standards and protocols. Nations such as Australia, Canada, Japan, and the United Kingdom have already expressed intentions to build independent SSA systems that are nevertheless interoperable with international frameworks [need citation]. This model allows countries to preserve their sovereignty—retaining their own tracking networks, analytical methods, and decision-making authority—while ensuring their data can “plug into” a shared global platform. In practice, this means each government could run its own SSA system domestically but also choose to upload selected orbital information, such as satellite registries or debris tracking data, into the SaaS platform. Once uploaded, the data is normalized and displayed alongside contributions from other countries, increasing the SSA’s capabilities in identifying potential collisions, congestion zones, or long-term sustainability risks in a way that no single nation could achieve alone.


Crucially, the SaaS platform supports tiered data-sharing agreements, so each participant grants viewing permissions and alerts according to its requirements. For instance, a country may decide to make its active satellite catalog publicly visible, share conjunction alerts with trusted partners only, and keep precise maneuver plans restricted to internal use. This approach addresses the concerns of achieving greater transparency and increased confidence in collision predictions, while protecting national security. 


Benefits of the System:
1.	By letting countries decide their level of disclosure, the system lowers political barriers to participation while increasing the overall volume and quality of global orbital data made publicly available.
2.	Participation provides tangible benefits to each country. By contributing to the system, governments gain access to higher-quality conjunction warnings, better situational awareness of crowded orbits, and the ability to verify or cross-check information provided by others. This reduces reliance on a single foreign system, which is a growing concern for countries worried about over-dependence on U.S. data. 
3.	Participation builds international trust and transparency, as all parties can see how their data contributes to a collective orbital “map.” 
4.	Countries retain their independence, safeguard their national interests, and strengthen their own SSA capabilities, as they benefit from the efficiencies and global reach of a cooperative SaaS-based STM platform.
