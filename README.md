# DDP-unibz-project-18697
Development of Data Products - Project Repository - 18697

This project conists of a product development for displaying Covid-19 cases per country, along with the government responses indicators. The project is based on the 3rx lab assignment of the Development of Data Products session on 2021/2022. The project is conducted individually, and the developed work is documented in this GitHub repository.

The developed code, together with the data sources, the planning boards and methodology diagrams are contained in the repository, located at their dedicated directories. The project is intended to be divided into branches, each one of them reflecting the work done in an iteration.

## Project Report

### Context

COVID-19 shaped our current lifestyle and changed the health measurements forever. The actual decade has seen several cases of people getting affected by the coronavirus pandemic, and special attention and priority should be given to every health, government and involved research areas institutions. Data is everywhere, is generated every day from an infinite number of sources and is on constant processing by machines programmed by the responsible professional groups. 

When relating data over a certain period, time series data is the core of analysis. Thus, time series data related to COVID-19 cases is collected by multiple organizations and ready to be retrieved, filtered, processed and visualized for human understanding. After all, the purpose of working with data is the benefit of the human well-being, by prevention and smart decision-making after conclusions have been proposed with the working data.

All the personnel interacting directly with health prevention, those being health care professionals, researchers, and government experts, need a user-friendly way to access real-time critical data regarding the monitoring of the different cases at any timeframe in any specific region or country. As collected information comes in form of time series data, it is the job of the proper data analysts, engineers and other data-oriented members to properly load and merge the data from different sources, clean and filter the data, aggregate and transform the data, and present it to the customer via clear visualizations or inferred conclusions from hypotheses for supporting governments and involved institutions in decision making related to the COVID-19 situation.

### Starting Point

During pandemic, every newspaper, website, television broadcast and any other communication source has presented the statistics for a city, region, or country of interest regarding the number of cases, the number of deceased and number or recovered people. There has been in most of the cases a common data source: the Johns Hopkins University. This research and academic institution, located in Baltimore, United States, has been always a leading reference point for reliable statistics about most of the political, health, and science aspects of the entire world. Therefore, the **Johns Hopkins University Center for Systems Science and Engineering (JHU CSSE)** has shared their knowledge data on a public GitHub repository. The available source aggregates pandemic data from primary sources, such as the World Health Organization, national, and regional public health institutions. 

Another source is the **Oxford COVID-19 Government Response Tracker (OxCGRT)**. It collects systematic information on policy measures that governments have taken to tackle the pandemic, they are adapted on a scale to reflect the extent of government action, and scores are aggregated as policy indexes. The summarized index is called a **Stringency Index (SI)**. Both data sources can be merged for creating a robust data frame that is going to be used for retrieving any data selection for visualization about the available variables at any region of interest for a given timeframe selection.

### Functional Objective

The objective of creating a data product with source information about the coronavirus cases is to aid the customers in reacting the smartest way possible, this meaning in applying, freezing or suspending policies and restrictions, always prioritizing the health of the population. A shift on how data analysis and visualization methodologies are executed under time pressure has been introduced after the pandemic situation, as nowadays a significant load of data is on the market ready to be processed and presented to end-users, allowing the creation of data products related to the monitoring of the COVID-19 cases, via web applications, key visualizations inside slide presentations, real-time software products, and more interesting alternatives.

The conducted project intends to track and compare government responses to the coronavirus outbreak by collecting and classifying different measures used by government bodies around the world. In short, the developed product should:
  -	collect and integrate pandemic and government responses from multiple sources
  -	merge, filter, clean and aggregate the collected data by different chosen criteria
  -	present the data to the customer via visualizations and found insights

The product focuses heavily on how governments determine the immediacy of restrictions and prevention regulations, this measured by the computed Stringency Index. A comparison of different government entities, different countries, is to be carried out by collecting, aggregating and presenting time series data. The product main priorities are listed below:
1.	Display **epidemic** and **Stringency Index** evolution over a selected region or country through time
2.	Elaborate comparisons of **cases, death and recovered patients**, between two selected regions or countries given a time window

The tools to use for developing the product idea are given as free choice options. As Python is the most popular programming language, and it has several user-friendly packages for creating visualizations and user interfaces, it is the chosen solution for the backbone of the project.

### Non-Functional Objective

During product design stage, there are important requirements that should be taken into account, listed as non-functional objectives, they do not describe any product functionality that is reflected in code data preprocessing, data filtering, data aggregation or data visualization, but more in how the product can be easily adaptable to unforeseen changes and information updates without the need to modify the core blocks of code, which is normally presented as class modules, class methods or independent functions:

•	Data is collected from different sources, meaning that the retrieved information can be of any data format, making the product stage of data collection more complicated. By design principle, every class, module, or function in the program should have just one dedicated purpose. The clear separation of functional responsibilities is related to the **Single Responsibility Principle (SRP)**, part of the well-known SOLID design principles for object-oriented software products.

•	The produced code should be designed to be extensible for additional data sources and for any new user query, as the user’s data of interest can change as the pandemic situation is in constant evolution and the implied government bodies can implement new regulations. The capability to be easily extended relies on the **Open-Closed Principle (OCP)** from the SOLID design principles.

### Project Overview

Every project implementation, regarding its scope, background and research focus should be preceded by a planning phase, where the overview questions should be formulated: What is the goal of this project? How the project should be split into tasks and subtasks? Who are the team members and which tasks are assigned to each partner? How to validate the developed product?

The planning process starts with a sketch of brainstorming ideas for answering the previous questions, which could be written in a notebook, a whiteboard, any software organizing tool. The information should be clear and available to every team member, as well for the end-user. As there is no need to reinvent the wheel, the product development methodology can be referenced from sources related to product and project management, where experienced people can state how a product planning should be executed.

### Data Sources

The product uses two main data sources: the Johns Hopkins University Center for Systems Science and Engineering (JHU CSSE), and the Blavatnik School of Government, a research and academic department of the University of Oxford. Both institutions provide the data in form of CSV tables which are easily readable by any chosen programming language package, along with written reports and user guides for data explanation. The data is available in their dedicated GitHub repositories, for which references [7] and [8] point to the data used on the conducted project.

•	**JHU CSSE** data provides daily and cumulative information about Covid-19 cases, for confirmed, death and recovered patients. Starting from January 22, 2020, and covering 192 countries, the cumulative and daily data can be merged for providing interesting visualizations about how registered cases have been evolving across different countries.

•	The **Oxford COVID-19 Government Response Tracker (OxCGRT)** provides the calculated Stringency Index (SI) across time on 185 countries, starting from January 22, 2020. As mentioned on the Chapter 2, the index is derived from the government responses about implemented regulations and restrictions on different aspects, like public transportation, events organization, workplace closures and travel measurements.

As for any data analysis project, the collected data runs a cleaning and filtering process, where special attention is put on non-available and missing data values, and that every column is independent from each other. Moreover, country names must match on the merging process, so that information does not get duplicated, altering the aggregation process. Data collection, preprocessing, aggregation and visualization steps are executed in a Python environment.

### Planning

The project planning kicks off with a brainstorming session for the product features. The product functional objective is clearly described in the first chapter, and then the product feature planning should be executed according to the user requirements.

A prioritization matrix containing the product feature ideas is constructed to have an overview of how complete the product features should be. The product has a functional feature which the end user requires, but additional enhancements could be done to enhance the product. The matrix is divided by effort and user value, displaying with features are considered important or not, and which features take more time to be completed.

A set of user stories are defined for the product development, which are split into two iterations. The chosen framework is the Kanban Board, for which web frameworks like Trello and Whimsical are used for the product planning and task management. The Kanban Boards are suppose to change per user story execution and completion, so the Kanban Boards organized in Trello for planning and for each user stories are shared in the repository.

**Planning Phase**

https://trello.com/b/viV1M5M5/kanban-board-planning-stage
