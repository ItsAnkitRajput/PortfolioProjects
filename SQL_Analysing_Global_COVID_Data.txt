-- Analysing Covid Data

SELECT *
FROM PORTFOLIO.dbo.CovidDeaths
WHERE continent IS NOT NULL
ORDER BY 3,4

SELECT *
FROM PORTFOLIO.dbo.CovidVaccinations
ORDER BY 3,4


------------------------------------------------------------
-- looking at total_cases vs total_deaths
-- shows chance of dying in percentage

SELECT location, date, total_cases, total_deaths, (total_deaths/total_cases)*100 AS "death_percentage"
FROM PORTFOLIO.dbo.CovidDeaths
WHERE location LIKE '%INDIA%'
ORDER BY 1,2


-------------------------------------------------------------------
-- looking at total_cases vs population
-- shows what percentage of population got covid

SELECT location, date, population, total_cases, (total_cases/population)*100 AS "death_percentage"
FROM PORTFOLIO.dbo.CovidDeaths
WHERE location LIKE '%INDIA%'
ORDER BY 1,2


------------------------------------------------------------------------------------------------------------
-- looking at infection count and percentage of population infected in each location in descending order

SELECT Location, MAX(total_cases) AS HighestInfectionCount, MAX((total_cases)/population)*100 as PercentagePopulationInfected
FROM PORTFOLIO..CovidDeaths
WHERE continent IS NOT NULL
GROUP BY location
ORDER BY PercentagePopulationInfected DESC

---------------------------------------------------------------------------------
-- showing countries with highest death_count per population

SELECT location, MAX(cast(total_deaths as bigint)) AS total_death_count, population
FROM PORTFOLIO..CovidDeaths
WHERE continent is not null
GROUP BY location, population
ORDER BY total_death_count DESC

--------------------------------------------------------------------------
-- showing continents with highest death_count per population
-- continent column had incorrect counts, so we filtered correct counts from locations column

SELECT location AS continent, MAX(cast(total_deaths as bigint)) AS total_death_count, population
FROM PORTFOLIO..CovidDeaths
WHERE continent is null
GROUP BY location, population
ORDER BY total_death_count DESC

---------------------------------------------------
-- GLOBAL NUMBERS

SELECT date, SUM(new_cases) AS cases, SUM(cast(new_deaths AS bigint)) AS deaths, SUM(cast(new_deaths AS bigint))/SUM(new_cases)*100 AS "death_percentage"
FROM PORTFOLIO.dbo.CovidDeaths
--WHERE location LIKE '%INDIA%'
WHERE continent IS NOT NULL
GROUP BY date
ORDER BY 1,2


SELECT SUM(new_cases) AS cases, SUM(cast(new_deaths AS bigint)) AS deaths, SUM(cast(new_deaths AS bigint))/SUM(new_cases)*100 AS "death_percentage"
FROM PORTFOLIO.dbo.CovidDeaths
--WHERE location LIKE '%INDIA%'
WHERE continent IS NOT NULL
--GROUP BY date
ORDER BY 1,2

-------------------------------------------------------
-- looking at total population vs vaccinations

SELECT dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations
FROM CovidDeaths AS dea
JOIN CovidVaccinations AS vac
	ON dea.location = vac.location
	AND dea.date = vac.date
WHERE dea.continent IS NOT NULL
ORDER BY 2, 3

------------------------------------------------------------------------
-- creating a rolling count of total vaccinated people per day

SELECT dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations
, SUM(CAST(vac.new_vaccinations AS INT)) OVER (PARTITION BY dea.location ORDER BY dea.location, dea.date) AS RollingPeopleVaccinated
FROM PORTFOLIO.dbo.CovidDeaths AS dea
JOIN PORTFOLIO.dbo.CovidVaccinations AS vac
	ON dea.location = vac.location
	AND dea.date = vac.date
WHERE dea.continent IS NOT NULL
ORDER BY 2, 3

----------------------------------
-- Use CTE

WITH PopVsVac (Continent, Location, Date, Population, New_Vaccinations, RollingPeopleVaccinated)
AS
(
SELECT dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations
, SUM(CAST(vac.new_vaccinations AS INT)) OVER (PARTITION BY dea.location ORDER BY dea.location, dea.date) AS RollingPeopleVaccinated
FROM PORTFOLIO.dbo.CovidDeaths AS dea
JOIN PORTFOLIO.dbo.CovidVaccinations AS vac
	ON dea.location = vac.location
	AND dea.date = vac.date
WHERE dea.continent IS NOT NULL
)
SELECT *, (RollingPeopleVaccinated/Population)*100 AS PerecentPopaccincated
FROM PopVsVac

------------------------------------
-- Temp Table

DROP TABLE IF exists #PercentPopulationVaccinated
CREATE TABLE #PercentPopulationVaccinated
(
continent nvarchar(255),
location nvarchar(255),
date datetime,
population numeric,
new_vaccination numeric,
RollingPeopleVaccinated numeric
)

Insert into #PercentPopulationVaccinated
SELECT dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations
	, SUM(CAST(vac.new_vaccinations AS INT)) OVER (PARTITION BY dea.location ORDER BY dea.location, dea.date) AS RollingPeopleVaccinated
FROM PORTFOLIO.dbo.CovidDeaths AS dea
JOIN PORTFOLIO.dbo.CovidVaccinations AS vac
	ON dea.location = vac.location
	AND dea.date = vac.date
WHERE dea.continent IS NOT NULL


SELECT *, (RollingPeopleVaccinated/Population)*100 AS PerecentPopVaccincated
FROM #PercentPopulationVaccinated

---------------------------------------------------
-- Creating view to store data for later

CREATE VIEW PercentPopulationVaccinated AS
SELECT dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations
	, SUM(CAST(vac.new_vaccinations AS INT)) OVER (PARTITION BY dea.location ORDER BY dea.location, dea.date) AS RollingPeopleVaccinated
FROM PORTFOLIO.dbo.CovidDeaths AS dea
JOIN PORTFOLIO.dbo.CovidVaccinations AS vac
	ON dea.location = vac.location
	AND dea.date = vac.date
WHERE dea.continent IS NOT NULL


SELECT *
FROM PORTFOLIO.dbo.CovidDeaths
WHERE continent IS NOT NULL
ORDER BY 3,4

SELECT *
FROM PORTFOLIO.dbo.CovidVaccinations
ORDER BY 3,4


--------------------------------------------------------
-- looking at total_cases vs total_deaths
-- shows chance of dying in percentage

SELECT location, date, total_cases, total_deaths, (total_deaths/total_cases)*100 AS "death_percentage"
FROM PORTFOLIO.dbo.CovidDeaths
WHERE location LIKE '%INDIA%'
ORDER BY 1,2


------------------------------------------------------
-- looking at total_cases vs population
-- shows what percentage of population got covid

SELECT location, date, population, total_cases, (total_cases/population)*100 AS "death_percentage"
FROM PORTFOLIO.dbo.CovidDeaths
WHERE location LIKE '%INDIA%'
ORDER BY 1,2


--------------------------------------------------------------------------------------------------------------
-- looking at infection count and percentage of population infected in each location in descending order

SELECT Location, MAX(total_cases) AS HighestInfectionCount, MAX((total_cases)/population)*100 as PercentagePopulationInfected
FROM PORTFOLIO..CovidDeaths
WHERE continent IS NOT NULL
GROUP BY location
ORDER BY PercentagePopulationInfected DESC

-------------------------------------------------------------------
-- showing countries with highest death_count per population

SELECT location, MAX(cast(total_deaths as bigint)) AS total_death_count, population
FROM PORTFOLIO..CovidDeaths
WHERE continent is not null
GROUP BY location, population
ORDER BY total_death_count DESC

---------------------------------------------------------------------
-- showing continents with highest death_count per population
-- continent column had incorrect counts, so we filtered correct counts from locations column

SELECT location AS continent, MAX(cast(total_deaths as bigint)) AS total_death_count, population
FROM PORTFOLIO..CovidDeaths
WHERE continent is null
GROUP BY location, population
ORDER BY total_death_count DESC

---------------------------------
-- GLOBAL NUMBERS

SELECT date, SUM(new_cases) AS cases, SUM(cast(new_deaths AS bigint)) AS deaths, SUM(cast(new_deaths AS bigint))/SUM(new_cases)*100 AS "death_percentage"
FROM PORTFOLIO.dbo.CovidDeaths
--WHERE location LIKE '%INDIA%'   --To get stats from India
WHERE continent IS NOT NULL
GROUP BY date
ORDER BY 1,2


SELECT SUM(new_cases) AS cases, SUM(cast(new_deaths AS bigint)) AS deaths, SUM(cast(new_deaths AS bigint))/SUM(new_cases)*100 AS "death_percentage"
FROM PORTFOLIO.dbo.CovidDeaths
--WHERE location LIKE '%INDIA%'
WHERE continent IS NOT NULL
--GROUP BY date
ORDER BY 1,2

-----------------------------------------------------
-- looking at total population vs vaccinations

SELECT dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations
FROM CovidDeaths AS dea
JOIN CovidVaccinations AS vac
	ON dea.location = vac.location
	AND dea.date = vac.date
WHERE dea.continent IS NOT NULL
ORDER BY 2, 3

-------------------------------------------------------------------------
-- creating a rolling count of total vaccinated people per day

SELECT dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations
	, SUM(CAST(vac.new_vaccinations AS INT)) OVER (PARTITION BY dea.location ORDER BY dea.location, dea.date) AS RollingPeopleVaccinated
FROM PORTFOLIO.dbo.CovidDeaths AS dea
JOIN PORTFOLIO.dbo.CovidVaccinations AS vac
	ON dea.location = vac.location
	AND dea.date = vac.date
WHERE dea.continent IS NOT NULL
ORDER BY 2, 3

------------------------
-- Using CTE

WITH PopVsVac (Continent, Location, Date, Population, New_Vaccinations, RollingPeopleVaccinated)
AS
(
SELECT dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations
	, SUM(CAST(vac.new_vaccinations AS INT)) OVER (PARTITION BY dea.location ORDER BY dea.location, dea.date) AS RollingPeopleVaccinated
FROM PORTFOLIO.dbo.CovidDeaths AS dea
JOIN PORTFOLIO.dbo.CovidVaccinations AS vac
	ON dea.location = vac.location
	AND dea.date = vac.date
WHERE dea.continent IS NOT NULL
)
SELECT *, (RollingPeopleVaccinated/Population)*100 AS PerecentPopaccincated
FROM PopVsVac

-------------------
-- Temp Table

DROP TABLE IF exists #PercentPopulationVaccinated
CREATE TABLE #PercentPopulationVaccinated
(
continent nvarchar(255),
location nvarchar(255),
date datetime,
population numeric,
new_vaccination numeric,
RollingPeopleVaccinated numeric
)

Insert into #PercentPopulationVaccinated
SELECT dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations
	, SUM(CAST(vac.new_vaccinations AS INT)) OVER (PARTITION BY dea.location ORDER BY dea.location, dea.date) AS RollingPeopleVaccinated
FROM PORTFOLIO.dbo.CovidDeaths AS dea
JOIN PORTFOLIO.dbo.CovidVaccinations AS vac
	ON dea.location = vac.location
	AND dea.date = vac.date
WHERE dea.continent IS NOT NULL


SELECT *, (RollingPeopleVaccinated/Population)*100 AS PerecentPopVaccincated
FROM #PercentPopulationVaccinated

---------------------------------------------------
--Creating view to store data for later

CREATE VIEW PercentPopulationVaccinated AS
SELECT dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations
	, SUM(CAST(vac.new_vaccinations AS INT)) OVER (PARTITION BY dea.location ORDER BY dea.location, dea.date) AS RollingPeopleVaccinated
FROM PORTFOLIO.dbo.CovidDeaths AS dea
JOIN PORTFOLIO.dbo.CovidVaccinations AS vac
	ON dea.location = vac.location
	AND dea.date = vac.date
WHERE dea.continent IS NOT NULL





