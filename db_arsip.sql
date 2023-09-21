-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Sep 21, 2023 at 04:43 PM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `db_arsip`
--

-- --------------------------------------------------------

--
-- Table structure for table `alembic_version`
--

CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `berkas_sm`
--

CREATE TABLE `berkas_sm` (
  `id` int(11) NOT NULL,
  `tanggal_diterima` date NOT NULL,
  `bagian` enum('pelayanan publik','sub bagian perencanaan','bendahara','sub bagian ketertiban','sub bagian pemerintah') NOT NULL,
  `file` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `berkas_sm`
--

INSERT INTO `berkas_sm` (`id`, `tanggal_diterima`, `bagian`, `file`) VALUES
(1, '2023-09-14', 'sub bagian perencanaan', ''),
(2, '2023-09-14', 'pelayanan publik', 'Science-ML-2015.pdf'),
(3, '2023-09-20', 'pelayanan publik', 'CamScanner 05-09-2023 12.00.pdf');

-- --------------------------------------------------------

--
-- Table structure for table `surat_keluar`
--

CREATE TABLE `surat_keluar` (
  `id` int(11) NOT NULL,
  `no_surat` varchar(25) NOT NULL,
  `tanggal_dibuat` date NOT NULL,
  `jenis_surat` enum('surat pernyataan','surat ahli waris','surat keterangan tidak mampu','surat keterangan pernikahan') NOT NULL,
  `asal_instansi` varchar(30) NOT NULL,
  `ditujukan` varchar(100) NOT NULL,
  `perihal` varchar(100) NOT NULL,
  `file` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `surat_keluar`
--

INSERT INTO `surat_keluar` (`id`, `no_surat`, `tanggal_dibuat`, `jenis_surat`, `asal_instansi`, `ditujukan`, `perihal`, `file`) VALUES
(1, 'b/123', '2023-09-01', 'surat pernyataan', 'Kec.sanankulon', '', 'undangan', '');

-- --------------------------------------------------------

--
-- Table structure for table `surat_masuk`
--

CREATE TABLE `surat_masuk` (
  `id` int(11) NOT NULL,
  `asal_surat` varchar(25) NOT NULL,
  `no_surat` varchar(15) NOT NULL,
  `kode_wilayah` varchar(25) NOT NULL,
  `tanggal_surat` date NOT NULL,
  `tanggal_diterima` date NOT NULL,
  `perihal` varchar(255) NOT NULL,
  `keterangan` enum('pelayanan publik','sub bagian perencanaan','bendahara','sub bagian ketertiban','sub bagian pemerintah') NOT NULL,
  `file` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `surat_masuk`
--

INSERT INTO `surat_masuk` (`id`, `asal_surat`, `no_surat`, `kode_wilayah`, `tanggal_surat`, `tanggal_diterima`, `perihal`, `keterangan`, `file`) VALUES
(1, 'unu b', '234', '254', '2023-09-13', '2023-09-13', 'undangan', 'sub bagian perencanaan', '');

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `username` varchar(25) NOT NULL,
  `password` varchar(255) NOT NULL,
  `email` varchar(25) NOT NULL,
  `foto` varchar(255) NOT NULL,
  `jabatan` varchar(25) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id`, `username`, `password`, `email`, `foto`, `jabatan`) VALUES
(1, 'admin1', 'pbkdf2:sha256:600000$WtcaFX200t3ihZOK$4ee4cad263b8cab04e0b4a1a0ed07e585f158196a9c086e788c8d66686107967', '123@gmail.com', '', '');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `alembic_version`
--
ALTER TABLE `alembic_version`
  ADD PRIMARY KEY (`version_num`);

--
-- Indexes for table `berkas_sm`
--
ALTER TABLE `berkas_sm`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `surat_keluar`
--
ALTER TABLE `surat_keluar`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `surat_masuk`
--
ALTER TABLE `surat_masuk`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `berkas_sm`
--
ALTER TABLE `berkas_sm`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `surat_keluar`
--
ALTER TABLE `surat_keluar`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `surat_masuk`
--
ALTER TABLE `surat_masuk`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
