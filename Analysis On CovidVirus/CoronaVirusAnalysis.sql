--  Table1 will have the total death details all over the world
DESCRIBE coviddeath;
select * from coviddeath LIMIT 5;



-- Total Cases in India and United States till now
select sum(total_cases) as sum_total_cases from coviddeath where location='India';

select sum(total_cases) as sum_total_cases from coviddeath where location='United States';



--  Table2 will have the total vaccination details all over the world

DESCRIBE covidvaccination;

select * from covidvaccination limit 5;

select  date,location,round(convert(positive_rate,FLOAT)*100,2) as 'Positive rate' from covidvaccination where positive_rate not in ('') limit 5;



-- Select Data that we are going to be starting with

Select Location, date, total_cases, new_cases, total_deaths, population
From CovidDeath
Where continent is not null AND location='India'
order by 1,2;


-- Total Cases vs Total Deaths (Death Percentage of India)

Select Location, date, total_cases,total_deaths, (total_deaths/total_cases)*100 as DeathPercentage
From CovidDeath
Where location='India' 
order by DeathPercentage desc;



-- Countries with Highest Death Count per Population
-- Since I wanted to see the Highest Death Count of India that's why I have filter it where location is India

Select date,Location, MAX(cast(Total_deaths as DECIMAL)) as TotalDeathCount
From CovidDeath
Where continent is not null and location = 'India'
Group by Location
order by TotalDeathCount desc;



-- Showing the highest death count per population with continent

Select continent, MAX(cast(Total_deaths as DECIMAL)) as TotalDeathCount
From coviddeath
Where continent not in ('')  -- Here I have remove a continent who name is not mention
Group by continent
order by TotalDeathCount desc;



-- Total new cases, Total Death and Death Percentage all over the world till now

Select SUM(new_cases) as total_cases, SUM(cast(new_deaths as DECIMAL)) as total_deaths, SUM(cast(new_deaths as DECIMAL))/SUM(New_Cases)*100 as DeathPercentage
From CovidDeath
where continent is not null 
order by 1,2;


-- Using CTE to perform Calculation on Partition By to shows Percentage of Population that has recieved at least one Covid Vaccine

With PopulationvsVaccination (Continent, Location, Date, Population, New_Vaccinations, RollingPeopleVaccinated)
as
(
Select dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations
, SUM(CONVERT(vac.new_vaccinations,DECIMAL)) OVER (Partition by dea.Location Order by dea.location, dea.Date) as RollingPeopleVaccinated
From CovidDeath as dea
Join CovidVaccination as vac
	On dea.location = vac.location
	and dea.date = vac.date
where dea.continent is not null 
order by 2,3
)

-- Let us see our CTE and also adding one more attribute for showing the percentage of People Vaccinated per Population
Select *, (RollingPeopleVaccinated/Population)*100
From PopulationvsVaccination;

