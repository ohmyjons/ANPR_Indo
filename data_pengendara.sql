-- phpMyAdmin SQL Dump
-- version 4.6.6deb5
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Jun 12, 2021 at 06:42 PM
-- Server version: 10.3.27-MariaDB-0+deb10u1
-- PHP Version: 7.3.27-1~deb10u1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `data_pengendara`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`id`, `username`, `password`) VALUES
(1, 'siapa', '$2y$10$/V2g53AZzGG0TJieGfIAIOVVbCtO2UWr2mzp7ZgylX3MDR9kxjk6.'),
(2, 'admin', '$2y$10$JmaJwVzcNlpjk30tg8RPBe6HPG7CL5hcQmrPFRF7iJacAVf3iw63u'),
(3, 'admin1', '$2y$10$.SwfvJIYSJyYEvRhulAKH.nqhXYLqah8euR6bsP8uA0n.NjV5Q/mu');

-- --------------------------------------------------------

--
-- Table structure for table `data`
--

CREATE TABLE `data` (
  `id` int(11) NOT NULL,
  `date` datetime NOT NULL,
  `name` text NOT NULL,
  `RFID` text NOT NULL,
  `plate` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `data`
--

INSERT INTO `data` (`id`, `date`, `name`, `RFID`, `plate`) VALUES
(1, '2021-06-11 00:00:00', 'Ahmad', 'YGH521I', 'W7689GH'),
(2, '2021-06-11 00:00:00', 'Ahmad', 'YGH521I', 'W7689GH');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `ID` int(11) NOT NULL,
  `Nama` varchar(255) DEFAULT NULL,
  `Card` varchar(255) DEFAULT NULL,
  `Plat` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`ID`, `Nama`, `Card`, `Plat`) VALUES
(1, 'Mail Ismailun', '723GH', 'AB5592EG'),
(2, 'Ahmad bin Ahmed', 'TY890K', 'AA5627JT'),
(3, 'Jalaludin Kiara', 'YA098U', 'AD2914JG'),
(6, 'Sundari Kalimata', 'YFN890', 'W2347NM'),
(7, 'Regi Iyo', 'AWE43R', 'W4598PL'),
(8, 'Ponaryo Kastangel', 'LP906G', 'L9834JK'),
(9, 'Rizal Granada J', '9IUJ09', 'W6292JX');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `data`
--
ALTER TABLE `data`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`ID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admin`
--
ALTER TABLE `admin`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;
--
-- AUTO_INCREMENT for table `data`
--
ALTER TABLE `data`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
