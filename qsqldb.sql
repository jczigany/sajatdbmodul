-- phpMyAdmin SQL Dump
-- version 4.8.5
-- https://www.phpmyadmin.net/
--
-- Gép: 127.0.0.1
-- Létrehozás ideje: 2020. Ápr 18. 11:12
-- Kiszolgáló verziója: 10.1.38-MariaDB
-- PHP verzió: 7.3.3

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Adatbázis: `qsqldb`
--

-- --------------------------------------------------------

--
-- Tábla szerkezet ehhez a táblához `teszt2`
--

CREATE TABLE `teszt2` (
  `id` int(11) NOT NULL,
  `gyartmany` varchar(30) NOT NULL,
  `tipus` varchar(30) NOT NULL,
  `gyartasiev` int(11) NOT NULL,
  `futottkm` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- A tábla adatainak kiíratása `teszt2`
--

INSERT INTO `teszt2` (`id`, `gyartmany`, `tipus`, `gyartasiev`, `futottkm`) VALUES
(1, 'Skoda', 'Octavia', 2008, 210000),
(2, 'Volvo', 'S80', 2006, 201000),
(3, 'Renault', 'Megane II', 2004, 164000),
(4, 'Trabant', 'S601', 1982, 245000);

--
-- Indexek a kiírt táblákhoz
--

--
--
-- A tábla indexei `teszt2`
--
ALTER TABLE `teszt2`
  ADD PRIMARY KEY (`id`);

--
-- A kiírt táblák AUTO_INCREMENT értéke
--

--
-- AUTO_INCREMENT a táblához `teszt2`
--
ALTER TABLE `teszt2`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
