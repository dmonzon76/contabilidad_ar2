-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 09-06-2026 a las 23:30:26
-- Versión del servidor: 9.5.0
-- Versión de PHP: 7.4.33

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `biblos`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `authors_author`
--

CREATE TABLE `authors_author` (
  `id` bigint NOT NULL,
  `last_name` varchar(100) NOT NULL,
  `names` varchar(100) NOT NULL,
  `birth_date` date DEFAULT NULL,
  `death_date` date DEFAULT NULL,
  `written_books` longtext,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) DEFAULT NULL,
  `created_by_id` bigint DEFAULT NULL,
  `nationality_id` bigint DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `authors_author`
--

INSERT INTO `authors_author` (`id`, `last_name`, `names`, `birth_date`, `death_date`, `written_books`, `created_at`, `updated_at`, `created_by_id`, `nationality_id`) VALUES
(1, 'Borges', 'Jorge Luis', '1899-08-24', '1986-06-14', 'La Muerte y la Brujula', '2025-12-22 20:55:10.531000', NULL, 1, 1),
(2, 'Verne', 'Jules', '1828-02-08', '1905-03-24', 'Around the World in Eighty Days', '2025-12-23 16:24:52.240000', NULL, 1, 3),
(3, 'Luna', 'Felix', '1925-09-30', '2009-11-05', 'Peron y su Tiempo 1\r\nPeron y su Tiempo 2\r\nPeron y su Tiempo 3', '2025-12-23 18:11:17.571000', NULL, 1, 1),
(4, 'Acevedo', 'Evaristo', '1915-02-12', '1997-01-31', 'Antologia del Humor Español', '2025-12-23 18:13:24.666000', NULL, 1, 4),
(5, 'Greene', 'Graham', '1910-10-02', '1991-04-03', 'El Agente Confidencial', '2025-12-23 18:16:45.637000', NULL, 1, 2),
(6, 'Vallejo', 'Fernando', '1942-10-24', NULL, '', '2025-12-23 18:19:42.692000', NULL, 1, 5),
(7, 'Vives', 'Jaume Vicents', '1910-06-06', '1960-06-28', '', '2025-12-23 21:29:58.374000', NULL, 1, 4),
(8, 'Nin Frias', 'Alberto Teodoro', '1878-11-09', '1937-03-27', 'Homosexualismo Creador', '2025-12-23 21:32:27.595000', NULL, 1, NULL),
(9, 'Belloc', 'Hilaire', '1870-07-27', '1953-07-16', '', '2025-12-23 21:34:46.722000', NULL, 1, 2),
(10, 'Hebbel', 'Christian Freidrich', '1813-03-18', '1863-12-13', '', '2025-12-23 21:38:18.404000', NULL, 1, 6),
(11, 'Alvarez Satullano', 'Luis', '1879-12-08', '1952-05-12', '', '2025-12-23 21:40:59.484000', NULL, 1, 4),
(12, 'Anderson', 'Matthew Smith', '1922-05-23', '2006-02-08', '', '2025-12-23 21:47:12.742000', NULL, 1, 2),
(13, 'del Zotti', 'Carlos', '1964-09-25', '2020-06-19', '', '2025-12-23 21:51:30.772000', NULL, 1, 4),
(14, 'Sarmiento', 'Domingo Faustino', '1811-02-15', '1888-09-11', 'Recuerdos de Provincia', '2025-12-28 20:23:19.011000', NULL, 1, 1),
(15, 'Woolrich', 'Cornell', '1903-12-04', '1968-09-25', '', '2025-12-28 20:36:33.428000', NULL, 1, 18),
(17, 'Tredice', 'Jacinto', NULL, NULL, '', '2025-12-29 18:44:32.294000', NULL, 1, 16),
(18, 'Schelinger', 'Erna', NULL, NULL, 'Tradiciones y Costumbres Judias', '2025-12-29 18:55:58.431000', NULL, 1, 1),
(19, 'Somerset Maugham', 'William', '1874-01-24', '1965-12-16', 'El Collar de Perlas\r\nEl Fila de la Navaja', '2025-12-29 18:59:36.352000', NULL, 1, 2),
(20, 'Wilter', 'Emma', NULL, NULL, '', '2025-12-29 19:00:52.940000', NULL, NULL, 18),
(21, 'Gaume', 'C. A.', NULL, NULL, '', '2025-12-29 19:03:19.073000', NULL, NULL, NULL),
(22, 'Bronté', 'Emily', '1818-07-30', '1848-12-19', 'Wuthering Heighs', '2025-12-29 19:05:54.320000', NULL, 1, 2),
(23, 'Shaw', 'Bernard', '1856-07-26', '1950-11-02', 'Major Barbera\r\nPigmalion', '2025-12-29 19:30:36.536000', NULL, 1, 23),
(24, 'Halevy', 'Elie', '1870-09-08', '1937-08-21', 'A History of the People English', '2025-12-29 19:34:40.823000', NULL, 1, 3),
(25, 'Meredith', 'George', '1828-02-12', '1909-05-18', 'El Egoista', '2025-12-29 19:37:37.037000', NULL, 1, 2),
(26, 'Cooper Prichart', 'Arthur Henry', '1874-01-01', NULL, '', '2025-12-30 21:48:20.508000', NULL, 1, 2),
(27, 'Scott', 'Walter', '1771-08-15', '1832-09-21', '', '2025-12-30 21:50:21.417000', NULL, NULL, 24),
(28, 'Christie', 'Agatha', '1890-09-15', '1976-01-12', '', '2025-12-30 21:56:19.983000', NULL, 1, 2),
(29, 'Websters', 'Jean', '1876-07-24', '1916-06-11', '', '2025-12-31 17:35:23.149000', NULL, 1, 18),
(30, 'Dickens', 'Charles', '1812-02-07', '1870-06-09', '', '2025-12-31 17:37:45.935000', NULL, 1, 2),
(31, 'Maclagan', 'Eric', '1879-12-04', '1951-09-14', '', '2025-12-31 17:51:04.948000', NULL, 1, 2),
(32, 'Messie', 'Robert', '1929-01-05', '2019-12-02', '', '2025-12-31 21:04:30.983000', NULL, 1, 18),
(33, 'Speke', 'Joh Hanning', '1827-05-01', '1864-09-15', '', '2025-12-31 21:08:51.778000', NULL, 1, 2),
(34, 'McArthur', 'Tom', '1938-08-23', '2020-03-30', 'Lexicon of Contemporary English', '2026-01-09 22:53:09.959000', NULL, 1, 24),
(35, 'Collie', 'George', NULL, NULL, 'Higland Dress', '2026-01-09 23:03:02.035000', NULL, 1, 24),
(36, 'Brun', 'Theodore', NULL, NULL, '', '2026-01-10 19:12:02.104000', NULL, 1, 2),
(37, 'Thackeray', 'William Makepeace', '1811-07-18', '1863-12-24', 'Vanity Fair', '2026-01-10 19:20:43.216000', NULL, 1, 2),
(38, 'Augier', 'Francis R', NULL, NULL, '', '2026-01-10 20:00:35.135000', NULL, 1, 2),
(39, 'Mackin', 'R', NULL, NULL, 'Ingles para Medicos', '2026-01-10 21:04:20.614000', NULL, 1, 2),
(40, 'Massy', 'Cristian Louis de', '1949-01-17', NULL, 'Palace', '2026-01-10 21:09:12.031000', NULL, 1, 3),
(42, 'Olson', 'Keith', NULL, NULL, 'An Outline of American History', '2026-01-10 21:20:27.797000', NULL, 1, 18),
(44, 'Garza Bores', 'Jaime', NULL, NULL, 'Manual de Verbos Ingleses', '2026-01-10 21:42:39.125000', NULL, 1, 4),
(45, 'Iglesias', 'Maria Isabel', NULL, NULL, 'Gramatica Sucinta Lengua Inglesa', '2026-01-10 21:46:35.567000', NULL, 1, 4),
(46, 'Murphy', 'Raymond', '1946-10-03', NULL, 'English Grammar in Use', '2026-01-10 21:54:09.879000', NULL, NULL, 2),
(47, 'Swan', 'Michel', '1936-03-21', NULL, 'Practical English Usage', '2026-01-10 22:13:11.664000', NULL, 1, 2),
(48, 'Galbraith', 'Robert', '1965-07-31', NULL, '', '2026-01-11 21:21:02.663000', NULL, 1, 2),
(49, 'Ensseñat y Morell', 'Juan Bautista', '1854-01-01', '1922-01-01', 'Maria Antonieta Intima', '2026-01-13 20:21:56.556000', NULL, 1, 4),
(50, 'Crombie', 'Alistar Cameron', '1915-11-04', '1996-02-09', 'Historia de la Ciencia de San Agustin a Galileo', '2026-01-13 20:47:08.275000', NULL, 1, 25),
(51, 'Gonzalez Palenza', 'Angel', '1889-09-04', '1949-10-30', 'Historia de la España Musulmana', '2026-01-13 20:50:05.341000', NULL, 1, 4),
(52, 'Mitre', 'Bartolome', '1821-06-21', '1906-01-19', 'Historia de Belgrano', '2026-01-14 20:07:16.926000', NULL, 1, 1),
(53, 'Sthendal', 'Henri Beyle', '1783-01-23', '1842-03-23', 'La Cartuja de Paarme', '2026-01-14 20:13:04.690000', NULL, 1, 3),
(54, 'Santa Teresa de Jesus', 'Teresa Sanchez de Cepeda Davila', '1515-03-28', '1582-10-04', 'Epistolario', '2026-01-14 20:17:17.669000', NULL, 1, 4),
(56, 'Anonimo', 'Anonimo', '1000-01-01', '1000-01-01', '', '2026-01-14 20:21:26.557000', NULL, 1, NULL),
(57, 'Irwing', 'Washington', '1783-04-03', '1859-11-28', 'Cuentos de La Alhambra', '2026-01-14 20:46:07.690000', NULL, 1, 18),
(59, 'Feijoo', 'Benito Jeronimo', '1676-10-08', '1764-09-26', 'Cartas Eruditas', '2026-01-14 20:57:13.274000', NULL, 1, 4),
(61, 'Dostoyevski', 'Pyodor', '1821-11-11', '1881-02-09', 'Las Pobres Gentes', '2026-01-14 21:13:31.228000', NULL, 1, 10),
(62, 'Howard', 'Cecil', NULL, NULL, 'West African Explores', '2026-01-14 21:17:29.942000', NULL, 1, 2),
(63, 'Sanchez Perez', 'Jose A', NULL, NULL, 'Cien Cuentos Populares Españoles', '2026-01-14 21:23:00.977000', NULL, 1, 4),
(64, 'Kitto', 'Humphrey Davey Findley', '1897-02-06', '1982-01-21', 'Los Griegos', '2026-01-14 21:26:10.811000', NULL, 1, 2),
(65, 'Olivieri', 'Nicolas', NULL, NULL, 'El Almacen', '2026-01-14 21:30:05.710000', NULL, 1, 1),
(66, 'Chesterton', 'Gilbert Keith', '1874-05-29', '1936-06-14', 'El Candor del Pedre Brown', '2026-01-14 21:33:38.496000', NULL, 1, 2),
(67, 'McCarthy', 'Michel', NULL, NULL, 'English Vocabulary in Use', '2026-01-15 18:21:07.420000', NULL, 1, 2),
(68, 'Faith', 'Nicholas', '1933-07-06', '2018-09-26', 'Cuentas Cifradas', '2026-01-15 18:28:58.721000', NULL, 1, 2),
(69, 'Alboukrek', 'Aaron', '1953-06-23', NULL, 'Diccionario de Sinonimos y Antonimos', '2026-01-15 18:35:16.819000', NULL, 1, 22),
(70, 'Baroja', 'Pio', '1872-12-28', '1956-10-30', 'El Horroroso Crimen de Peñaranda del Campo', '2026-01-15 18:39:15.269000', NULL, 1, 4),
(71, 'Sejen', 'Juan Bautista', NULL, NULL, 'San Martin y la Tercera Invasion Inglesa', '2026-01-15 20:35:01.156000', NULL, 1, 1),
(72, 'Guy de Monpassant', 'Henry Renee Albert', '1850-08-05', '1893-07-06', 'El Adereso de Brillantes', '2026-01-15 20:38:56.729000', NULL, 1, 3),
(73, 'Cervantes Saavedra', 'Miguel', '1547-09-29', '1616-04-22', 'Don Quijote de la Mancha', '2026-01-15 20:44:11.943000', NULL, 1, 4),
(76, 'Meyer', 'Michel', '1950-11-11', '2022-05-23', 'El año que Cambió el Mundo', '2026-01-15 20:55:08.556000', NULL, 1, 3),
(79, 'Browne', 'Douglas', '1884-01-01', '1963-01-01', 'El Escalpelo de Scotlang Yard', '2026-01-15 21:01:52.580000', NULL, 1, 2),
(80, 'Arispe', 'Artemio del Valle', '1888-01-25', '1961-11-15', 'Historia de la Ciudad de Mexico', '2026-01-15 21:06:44.160000', NULL, 1, 22),
(81, 'Proust', 'Marcel', '1871-07-10', '1922-11-18', 'Sodoma y Gomorra', '2026-01-15 21:16:01.731000', NULL, 1, 3),
(82, 'Cronin', 'Archibal Joseph', '1896-07-19', '1981-01-06', 'Las Estrellas Miran Hacia Abajo', '2026-01-15 21:19:13.498000', NULL, 1, 2),
(83, 'Caseres', 'Julio', '1877-01-01', '1964-01-01', 'Diccionario Ideológico de la Lengua Española', '2026-01-15 21:24:05.245000', NULL, 1, 4),
(84, 'Saban', 'Mario Javier', '1966-02-12', NULL, 'Los Hebreos', '2026-01-29 18:57:33.217193', '2026-01-29 18:57:33.217213', 1, 1),
(85, 'Maritain', 'Jacques', '1882-11-18', '1973-04-28', 'Introduccion a la Filosofia', '2026-01-29 19:26:16.765650', '2026-01-29 19:26:16.765663', 1, 3),
(86, 'Palma', 'Ricardo', '1833-02-07', '1919-10-06', 'Tradiciones Peruanas', '2026-01-29 19:29:05.165851', '2026-01-29 19:29:05.165862', 1, 21),
(87, 'Lopez de Gomara', 'Francisco', '1511-02-02', '1559-12-02', 'Historia de la Conquista de Mexico', '2026-01-29 20:42:36.223624', '2026-01-29 20:42:36.223636', 1, 4),
(88, 'Flaubert', 'Gustavo', '1821-12-12', '1880-05-08', 'Madame Bovary', '2026-01-29 20:45:36.588773', '2026-01-29 20:45:36.588790', 1, 3),
(89, 'Fayt', 'Carlos Santiago', '1918-02-01', '2016-11-22', 'Por una Nueva Argentina', '2026-01-29 20:52:19.025713', '2026-01-29 20:52:19.025724', 1, 1),
(90, 'Lesage', 'Alain Rene', '1668-05-08', '1747-11-12', 'Gil Blas de Santillana', '2026-01-29 20:56:12.409827', '2026-01-29 20:56:12.409854', 1, 3),
(91, 'Dumas', 'Alejandro', '1802-07-24', '1870-12-05', 'Los Tres Mosqueteros', '2026-01-29 21:59:32.102364', '2026-01-29 21:59:32.102378', 1, 3),
(92, 'Benhamou', 'Olivia', NULL, NULL, 'El Libro de la Tranquilidad', '2026-01-29 22:07:53.826199', '2026-01-29 22:07:53.826213', 1, 3),
(93, 'Capdevila', 'Arturo', '1889-03-14', '1967-12-20', 'Babel y el Castellano', '2026-01-29 22:19:01.631793', '2026-01-29 22:19:01.631805', 1, 1),
(94, 'Rodriguez', 'Gregorio', NULL, NULL, 'El General Soler', '2026-01-29 22:22:45.916930', '2026-01-29 22:22:45.916945', 1, 1),
(95, 'Vasconcelos', 'Jose', '1882-02-28', '1959-06-30', 'Hernan Cortes', '2026-01-29 22:50:01.456591', '2026-01-29 22:50:01.456603', 1, 22),
(96, 'Sombart', 'Werner', '1863-01-19', '1941-05-18', 'El Burgues', '2026-01-29 22:59:24.486768', '2026-01-29 22:59:24.486779', 1, 6),
(97, 'Capparelli', 'Vicente', NULL, NULL, 'Recopilacion de Voces del Lunfardo', '2026-01-30 19:33:01.359083', '2026-01-30 19:33:01.359131', 1, 1),
(98, 'Decaux', 'Alain', '1925-07-23', '2016-03-16', 'La Historia Secreta de la Historia', '2026-01-30 19:36:20.630869', '2026-01-30 19:36:20.630891', 1, 3),
(99, 'Wallace', 'Richard Horatio Edgar', '1875-04-01', '1932-02-10', 'Novelas de Intriga', '2026-01-30 19:39:29.907761', '2026-01-30 19:39:29.907773', 1, 2),
(100, 'Steinbeck', 'John', '1902-02-27', '1968-12-20', 'Viñas de Ira', '2026-01-31 20:04:23.618737', '2026-01-31 20:04:23.618758', 1, 18),
(101, 'Doyle', 'Arthur Conan', '1859-05-22', '1930-07-07', 'Novelas de Aventuras', '2026-01-31 21:09:17.148668', '2026-01-31 21:09:17.148682', 1, 2),
(102, 'Hitchcock', 'Alfred', '1899-08-13', '1980-04-29', 'Mis Suspenses Favoritas', '2026-01-31 21:15:16.179395', '2026-01-31 21:15:16.179407', 1, 2),
(103, 'Becco', 'Horacio Jorge', '1924-10-28', '2005-10-26', 'Don Segundo Sombra', '2026-01-31 21:21:03.983623', '2026-01-31 21:21:03.983643', 1, 1),
(104, 'Gumilla', 'Jose', '1686-05-03', '1750-07-16', 'El Orinoco', '2026-01-31 21:27:45.413509', '2026-01-31 21:29:19.496113', 1, 4),
(105, 'Ferguson', 'Charles Elmo', '1928-09-07', '1972-01-14', 'Teoria Microeconomica', '2026-01-31 21:33:15.180005', '2026-01-31 21:33:15.180021', 1, 18),
(106, 'Colegio Graduados en Estadistica', 'Colegio', NULL, NULL, 'Tablas Estadisticas', '2026-01-31 21:35:55.029717', '2026-01-31 21:36:26.514658', 1, 1),
(107, 'Medina', 'Oscar', NULL, NULL, 'Costos Bancarios', '2026-02-01 18:37:15.992786', '2026-02-01 18:37:15.992800', 1, 1),
(108, 'Colaiocovo', 'Juan Luis', NULL, NULL, 'Tecnicas de Negociaciones', '2026-02-01 18:41:58.094500', '2026-02-01 18:41:58.094515', 1, 19),
(109, 'Busaniche', 'Jose Luis', '1892-09-12', '1959-01-01', 'Historia Argentina', '2026-02-01 18:45:12.345812', '2026-02-01 18:45:12.345842', 1, 1),
(110, 'Lazzati', 'Santiago', NULL, NULL, 'Ensayos sobre Teoria Contable', '2026-02-01 18:50:16.095114', '2026-02-01 18:50:16.095151', 1, 1),
(111, 'Rivera Pereyra', 'Carlos Alberto', NULL, NULL, 'Los Indicadores Economicos', '2026-02-01 18:53:34.609725', '2026-02-01 18:53:34.609737', 1, 1),
(112, 'Fowler Newton', 'Enrique', '1944-12-23', NULL, 'El Ajuste de Estados Contables por Inflacion', '2026-02-01 19:00:10.446453', '2026-02-01 19:00:10.446465', 1, 1),
(113, 'Yofre', 'Juan Bautista', '1946-12-16', NULL, 'El Escarmiento', '2026-04-25 21:24:06.586384', '2026-04-25 21:24:06.586384', 1, 1),
(114, 'Mercado', 'Silvia', '1959-06-08', NULL, 'El Relato Peronista', '2026-04-25 21:48:42.539592', '2026-04-25 21:48:42.539592', 1, 1),
(115, 'Reato', 'Ceferino', '1961-10-10', NULL, 'Disposición Final', '2026-04-25 22:01:44.686827', '2026-04-25 22:01:44.686827', 1, 1),
(116, 'Young', 'Gerardo', '1972-01-01', NULL, 'Codigo Stiuso', '2026-04-25 22:09:31.107110', '2026-04-25 22:09:31.107110', 1, 1),
(117, 'Santoro', 'Daniel', '1958-12-04', NULL, 'Los intocables', '2026-04-26 21:19:33.338298', '2026-04-26 21:19:33.338298', 1, 1),
(118, 'Majul', 'Luis', '1961-05-17', NULL, 'Los Dueños de la Argentina', '2026-04-26 21:22:12.898253', '2026-04-26 21:22:12.898253', 1, 1),
(119, 'Sebreli', 'Juan Jose', '1930-11-03', '2024-11-01', 'El malestar de la politica', '2026-04-26 21:33:36.134576', '2026-04-26 21:33:36.134576', 1, 1),
(120, 'Acuña', 'Marcelo Luis', '1950-12-16', NULL, 'El corralito populista', '2026-04-26 21:38:59.021223', '2026-04-26 21:38:59.021223', 1, 1),
(121, 'Sarlo', 'Beatriz', '1942-03-29', '2024-12-17', 'La Audacia y el Calculo', '2026-04-26 21:42:11.168284', '2026-04-26 21:42:11.168284', 1, 1),
(122, 'Rinaldi', 'Franco', '1980-01-01', NULL, 'Aerolineas Argentinas', '2026-04-26 22:05:58.271628', '2026-04-26 22:05:58.271628', 1, 1),
(123, 'Lanata', 'Jorge Ernesto', '1960-09-12', '2024-12-30', 'Argentinos', '2026-04-26 22:11:11.948891', '2026-04-26 22:11:11.948891', 1, 1),
(124, 'Grondona', 'Mariano', '1932-10-19', NULL, 'La Corrupcion', '2026-04-26 22:15:37.402017', '2026-04-26 22:15:37.402017', 1, 1),
(125, 'Aguirre', 'Osvaldo', '1964-01-01', NULL, 'Enemigos Publicos', '2026-04-26 22:24:57.781324', '2026-04-26 22:24:57.781324', 1, 1),
(126, 'Terragno', 'Rodolfo', '1943-11-16', NULL, 'San Martin', '2026-04-27 21:33:19.102304', '2026-04-27 21:33:19.102304', 1, 1),
(127, 'Johnson', 'Paul', '1928-11-02', '2023-01-12', 'Heroes', '2026-04-27 21:37:42.218133', '2026-04-27 21:37:42.218133', 1, 2),
(128, 'Garcia Hamilton', 'Jose Ignacio', '1943-11-01', '2009-06-18', 'Porque Crecen los Países', '2026-04-27 21:46:14.936727', '2026-04-27 21:46:14.936727', 1, 1),
(129, 'Aguinis', 'Marcos', '1935-01-13', NULL, 'El Elogio de la Culpa', '2026-04-27 22:06:02.438349', '2026-04-27 22:06:02.438349', 1, 1),
(130, 'Marx', 'Carlos', '1818-05-05', '1883-03-14', 'El Capital I y II', '2026-04-27 22:11:04.085829', '2026-04-27 22:11:04.085829', 1, 6),
(131, 'Motura', 'Giraldo', '1935-01-01', NULL, 'Aprender a curarte', '2026-05-01 21:46:21.786945', '2026-05-01 21:46:21.786945', 1, 1),
(132, 'Kazan', 'Elia', '1909-09-07', '2003-09-28', 'El Doble', '2026-05-02 19:54:49.600029', '2026-05-02 19:59:45.482927', 1, 26),
(134, 'Medina', 'Enrique', '1937-12-26', NULL, 'El Hombre del Corazón Caído', '2026-05-02 20:15:53.006650', '2026-05-02 20:15:53.006650', 1, 1),
(135, 'Solzhenitsyn', 'Alexander', '1918-12-11', '2008-08-03', 'Un día en la Vida de Iván Denisovich', '2026-05-02 20:24:04.102478', '2026-05-02 20:24:04.102478', 1, 10),
(136, 'Caparros', 'Martin', '1957-05-29', NULL, 'El Hambre', '2026-05-02 20:27:31.000175', '2026-05-02 20:27:31.000175', 1, 1),
(137, 'Botana', 'Helvio Ildefonso', '1915-10-14', '1990-02-20', 'Memorias\r\nTras los Dientes del Perro', '2026-05-02 21:35:20.935809', '2026-05-02 21:35:20.935809', 1, 1),
(138, 'Balzac', 'Honorato de', '1799-05-20', '1850-08-18', 'Eugenia Grandet\r\nLa Casa Nucigen\r\nCesar Birotteau', '2026-05-02 21:44:31.402266', '2026-05-02 21:44:31.402266', 1, 3),
(139, 'Harwicz', 'Arianna', '1977-12-13', NULL, 'Degenerado', '2026-05-02 22:09:16.950924', '2026-05-02 22:09:16.950924', 1, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `authors_nationality`
--

CREATE TABLE `authors_nationality` (
  `id` bigint NOT NULL,
  `name` varchar(100) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `created_by_id` bigint DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `authors_nationality`
--

INSERT INTO `authors_nationality` (`id`, `name`, `created_at`, `created_by_id`) VALUES
(1, 'Argentina', '2025-12-22 20:56:35.331000', 1),
(2, 'Inglaterra', '2025-12-22 20:56:50.671000', 1),
(3, 'Francia', '2025-12-22 20:57:00.540000', 1),
(4, 'España', '2025-12-23 18:14:30.642000', 1),
(5, 'Colombia', '2025-12-23 18:18:57.576000', 1),
(6, 'Alemania', '2025-12-27 18:44:04.108000', 1),
(7, 'Dinamarca', '2025-12-27 19:18:18.402000', 1),
(8, 'Suecia', '2025-12-27 19:18:27.296000', 1),
(9, 'Noruega', '2025-12-27 19:18:37.331000', 1),
(10, 'Rusia', '2025-12-27 19:19:04.664000', 1),
(11, 'Hungria', '2025-12-27 19:19:30.344000', 1),
(12, 'Polonia', '2025-12-27 19:19:42.901000', 1),
(13, 'Estonia', '2025-12-27 19:19:53.818000', 1),
(14, 'Lituania', '2025-12-27 19:20:02.707000', 1),
(15, 'Eslovenia', '2025-12-27 19:20:21.834000', 1),
(16, 'Italia', '2025-12-27 19:20:41.533000', 1),
(17, 'Grecia', '2025-12-27 19:20:55.102000', 1),
(18, 'Estados Unidos', '2025-12-28 20:41:41.166000', 1),
(19, 'Brazil', '2025-12-28 20:42:21.919000', 1),
(20, 'Chile', '2025-12-28 20:42:38.819000', 1),
(21, 'Peru', '2025-12-28 20:42:53.871000', 1),
(22, 'Mexico', '2025-12-28 20:43:19.293000', 1),
(23, 'Irlanda', '2025-12-29 19:31:07.740000', 1),
(24, 'Escocia', '2025-12-31 22:07:39.701000', 1),
(25, 'Australia', '2026-01-13 20:44:34.567000', 1),
(26, 'Turquia', '2026-05-02 19:55:51.395459', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 3, 'add_permission'),
(6, 'Can change permission', 3, 'change_permission'),
(7, 'Can delete permission', 3, 'delete_permission'),
(8, 'Can view permission', 3, 'view_permission'),
(9, 'Can add group', 2, 'add_group'),
(10, 'Can change group', 2, 'change_group'),
(11, 'Can delete group', 2, 'delete_group'),
(12, 'Can view group', 2, 'view_group'),
(13, 'Can add content type', 4, 'add_contenttype'),
(14, 'Can change content type', 4, 'change_contenttype'),
(15, 'Can delete content type', 4, 'delete_contenttype'),
(16, 'Can view content type', 4, 'view_contenttype'),
(17, 'Can add session', 5, 'add_session'),
(18, 'Can change session', 5, 'change_session'),
(19, 'Can delete session', 5, 'delete_session'),
(20, 'Can view session', 5, 'view_session'),
(21, 'Can add nationality', 7, 'add_nationality'),
(22, 'Can change nationality', 7, 'change_nationality'),
(23, 'Can delete nationality', 7, 'delete_nationality'),
(24, 'Can view nationality', 7, 'view_nationality'),
(25, 'Can add author', 6, 'add_author'),
(26, 'Can change author', 6, 'change_author'),
(27, 'Can delete author', 6, 'delete_author'),
(28, 'Can view author', 6, 'view_author'),
(29, 'Can add Book', 8, 'add_book'),
(30, 'Can change Book', 8, 'change_book'),
(31, 'Can delete Book', 8, 'delete_book'),
(32, 'Can view Book', 8, 'view_book'),
(33, 'Can add Publishing House', 9, 'add_publishinghouse'),
(34, 'Can change Publishing House', 9, 'change_publishinghouse'),
(35, 'Can delete Publishing House', 9, 'delete_publishinghouse'),
(36, 'Can view Publishing House', 9, 'view_publishinghouse'),
(37, 'Can add theme', 10, 'add_theme'),
(38, 'Can change theme', 10, 'change_theme'),
(39, 'Can delete theme', 10, 'delete_theme'),
(40, 'Can view theme', 10, 'view_theme'),
(41, 'Can add language', 11, 'add_language'),
(42, 'Can change language', 11, 'change_language'),
(43, 'Can delete language', 11, 'delete_language'),
(44, 'Can view language', 11, 'view_language'),
(45, 'Can add search', 12, 'add_search'),
(46, 'Can change search', 12, 'change_search'),
(47, 'Can delete search', 12, 'delete_search'),
(48, 'Can view search', 12, 'view_search'),
(49, 'Can add user', 13, 'add_user'),
(50, 'Can change user', 13, 'change_user'),
(51, 'Can delete user', 13, 'delete_user'),
(52, 'Can view user', 13, 'view_user'),
(61, 'Can add language', 28, 'add_language'),
(62, 'Can change language', 28, 'change_language'),
(63, 'Can delete language', 28, 'delete_language'),
(64, 'Can view language', 28, 'view_language');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `books_book`
--

CREATE TABLE `books_book` (
  `id` bigint NOT NULL,
  `title` varchar(200) NOT NULL,
  `location` varchar(100) NOT NULL,
  `publication_date` date DEFAULT NULL,
  `isbn` varchar(13) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `author_id` bigint NOT NULL,
  `language_id` bigint DEFAULT NULL,
  `publishing_house_id` bigint NOT NULL,
  `theme_id` bigint DEFAULT NULL,
  `updated_at` datetime(6) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `books_book`
--

INSERT INTO `books_book` (`id`, `title`, `location`, `publication_date`, `isbn`, `created_at`, `author_id`, `language_id`, `publishing_house_id`, `theme_id`, `updated_at`) VALUES
(1, 'Around the World in Eighty Days', 'dormitorio ventana 1 1', '1994-01-01', '9780140623680', '2025-12-23 16:28:31.554000', 2, 2, 1, 6, NULL),
(2, 'La Puta de Babilonia', 'living 1 1', '2007-01-01', '9789875802599', '2025-12-23 18:21:24.808000', 6, 1, 1, 1, NULL),
(3, 'Historia del Humor Español', 'living 1 1', '1957-01-01', NULL, '2025-12-23 22:00:59.258000', 4, 1, 3, 1, NULL),
(4, 'El Agente Confidencial', 'Living 1 1', '1955-01-01', NULL, '2025-12-23 22:02:32.564000', 5, 1, 4, 6, NULL),
(5, 'El Egoista', 'Living 1 1', '1945-01-01', NULL, '2025-12-23 22:04:32.626000', 25, 1, 4, 6, NULL),
(6, 'Historia de España y America', 'Living 1 1', '1957-01-01', '8431618671000', '2025-12-23 22:08:56.614000', 7, 1, 5, 1, NULL),
(7, 'El Caracter Ingles', 'Living 1 1', '1924-01-01', NULL, '2025-12-23 22:13:02.922000', 8, 1, 4, 1, NULL),
(8, 'Las Cruzadas', 'Living 1 1', '1944-01-01', NULL, '2025-12-23 22:18:07.772000', 9, 1, 4, 1, NULL),
(9, 'Judith', 'Living 1 1', '1944-01-01', NULL, '2025-12-23 22:19:45.292000', 10, 1, 4, 8, NULL),
(10, 'Romance y Canciones de España y America', 'Living 1 1', '1955-01-01', NULL, '2025-12-23 22:22:18.440000', 11, 1, 6, 9, NULL),
(11, 'La Europa del siglo XVIII', 'Living 1 1', '1968-01-01', NULL, '2025-12-23 22:23:48.816000', 12, 1, 7, 1, NULL),
(12, 'Brujeria y Magia en America', 'Living 1 1', '1977-01-01', '8401470171000', '2025-12-23 22:25:47.319000', 13, 1, 8, 7, NULL),
(13, 'Recuerdos de Provincia', 'dormitorio ventana 1 1', '1962-01-01', NULL, '2025-12-28 20:23:19.021000', 14, 1, 9, 1, NULL),
(14, 'Obras Escogidas', 'dormitorio ventana 1 1', '1968-04-01', '9041196315563', '2025-12-28 20:40:20.697000', 15, 1, 10, 11, NULL),
(15, 'Peron y su Tiempo 1', 'living 1 1', '1984-01-01', '9500702266000', '2025-12-29 15:30:09.851000', 3, 1, 2, 1, NULL),
(16, 'Peron y su Tiempo 2', 'living 1 1', '1985-01-01', '9500703130000', '2025-12-29 15:31:35.394000', 3, 1, 2, 1, NULL),
(17, 'Peron y su Tiempo 3', 'living 1 1', '1986-01-01', '9500703815000', '2025-12-29 15:32:53.392000', 3, 1, 2, 1, NULL),
(18, 'Antologia del Humor Español', 'living 1 1', '1957-01-01', NULL, '2025-12-29 15:54:49.250000', 4, 1, 3, 10, NULL),
(20, 'Historia de la Filosofia', 'dormitorio ventana 1 1', '1976-09-01', NULL, '2025-12-29 18:44:32.302000', 17, 1, 9, 1, NULL),
(21, 'La Muerte y la Brujula', 'dormitorio ventana 1 1', '1951-09-04', NULL, '2025-12-29 18:50:00.427000', 1, 1, 4, 6, NULL),
(22, 'Tradiciones y Costumbres Judias', 'dormitorio ventana 1 1', '1942-01-01', NULL, '2025-12-29 19:40:05.181000', 18, 1, 11, 9, NULL),
(23, 'El Filo de la Navaja', 'dormitorio ventana 1 1', '1944-04-01', NULL, '2025-12-29 19:44:24.139000', 19, 1, 12, 6, NULL),
(24, 'Historia de la Filosofia Grecia y Roma', 'dormitorio ventana 1 1', '1971-01-01', NULL, '2025-12-29 19:47:21.254000', 4, 1, 12, 1, NULL),
(25, 'Narracion Singular', 'dormitorio ventana 1 1', '1943-01-01', NULL, '2025-12-29 19:53:49.253000', 19, 1, 12, 6, NULL),
(26, 'El Collar de Perlas', 'dormitorio ventana 1 1', '1944-07-30', NULL, '2025-12-29 20:44:35.248000', 19, 1, 12, 6, NULL),
(27, 'Prose and Poetry', 'dormitorio ventana 1 1', '1935-01-01', NULL, '2025-12-29 20:45:56.936000', 20, 2, 14, 9, NULL),
(28, 'Select Readings', 'dormitorio ventana 1 1', '1972-01-01', NULL, '2025-12-29 20:47:07.664000', 21, 2, 15, 11, NULL),
(29, 'Wuthering Heights', 'dormitorio ventana 1 1', '1972-01-01', NULL, '2025-12-29 20:48:22.102000', 22, 2, 15, 11, NULL),
(30, 'Major Barbera', 'dormitorio ventana 1 1', '1944-01-01', NULL, '2025-12-29 20:49:48.848000', 23, 2, 16, 11, NULL),
(31, 'A History of the People English', 'dormitorio ventana 1 1', '1937-01-01', NULL, '2025-12-29 20:51:07.396000', 24, 2, 17, 1, NULL),
(32, 'Pigmalion', 'dormitorio ventana 1 1', '1942-01-01', NULL, '2025-12-29 20:52:11.263000', 23, 2, 16, 8, NULL),
(33, 'The Buccaneers', 'dormitorio ventana 1 1', '1929-01-01', NULL, '2025-12-30 21:48:20.519000', 26, 2, 18, 6, NULL),
(34, 'Ivanhoe', 'dormitorio ventana 1 1', '1939-01-01', NULL, '2025-12-30 21:50:21.425000', 27, 2, 21, 11, NULL),
(35, 'Daddy long Legs', 'dormotorio ventana 1 1', '1934-01-01', NULL, '2025-12-31 17:35:23.162000', 29, 2, 19, 11, NULL),
(36, 'Great Spectations', 'dormitorio ventana 1 1', '1997-01-01', '5822752020000', '2025-12-31 17:37:45.943000', 30, 2, 20, 11, NULL),
(37, 'The Bayeux Tapextry', 'dormitorio ventana 1 1', '1945-01-01', NULL, '2025-12-31 17:51:04.956000', 31, 2, 16, 1, NULL),
(38, 'Ten Moderns Nistery Stories', 'dormitorio ventana 1 1', '1945-01-01', NULL, '2025-12-31 18:14:57.775000', 28, 2, 15, 11, NULL),
(39, 'Nicholas and Alexandra', 'dormitorio ventana 1 1', '1952-01-01', NULL, '2025-12-31 21:04:30.992000', 32, 2, 21, 1, NULL),
(40, 'Journal of Discovery The Nile', 'dormitorio ventana 1 1', '1912-01-01', NULL, '2025-12-31 21:08:51.787000', 33, 2, 22, 1, NULL),
(41, 'Ten Modern Mystery Histories', 'dormitorio ventana 1 1', '1972-01-01', NULL, '2026-01-09 22:48:06.526000', 28, 2, 26, 6, NULL),
(42, 'Lexicon of Contemporary English', 'dormitorio ventana 1 1', '1986-01-01', '0582555272000', '2026-01-09 22:50:58.728000', 34, 2, 23, 12, NULL),
(43, 'Higland Dress', 'dormitorio ventana 1 1', '1948-01-01', NULL, '2026-01-09 23:03:02.042000', 35, 2, 24, 1, NULL),
(44, 'The International Dictionary of Sign Language', 'dormitorio ventana 1 1', '1969-01-01', NULL, '2026-01-10 19:02:03.820000', 36, 2, 25, 12, NULL),
(45, 'Traveling a European Journey', 'dormitorio ventana 1 1', '1969-01-01', NULL, '2026-01-10 19:13:56.149000', 21, 2, 15, NULL, NULL),
(46, 'Vanity Fair', 'dormitorio ventana1 1', '1967-01-01', NULL, '2026-01-10 19:20:43.224000', 37, 2, 26, 6, NULL),
(47, 'The Making of The West Indies', 'dormitorio ventana 1 1', NULL, '0582763045000', '2026-01-10 20:00:35.143000', 38, 2, 27, 1, NULL),
(48, 'Pierwik Papers', 'dormitorio ventana 1 1', '1889-01-01', NULL, '2026-01-10 20:46:47.764000', 30, 2, 12, 6, NULL),
(49, 'Barnaby Rouge', 'dormitorio ventana 1 1', '1189-01-01', NULL, '2026-01-10 20:47:38.696000', 30, 2, 12, 6, NULL),
(50, 'Sketches By Boz', 'dormitorio ventana 1 1', '1889-01-01', NULL, '2026-01-10 20:51:17.682000', 30, 2, 12, 6, NULL),
(51, 'Ingles para Medicos', 'dormitorio ventana 1 1', '1949-01-01', NULL, '2026-01-10 21:04:20.623000', 39, 2, 20, 12, NULL),
(52, 'Palace', 'dormitorio ventana 1 1', '1986-01-01', NULL, '2026-01-10 21:09:12.040000', 40, 2, 12, 1, NULL),
(54, 'Manual de Verbos Ingleses', 'dormitorio ventana 1 1', '1962-01-01', '9681309995000', '2026-01-10 21:42:39.133000', 44, 2, 13, 12, NULL),
(55, 'Gramatica Sucinta Lengua Inglesa', 'dormitorio ventana 1 1', '1985-01-01', '8425408075000', '2026-01-10 21:46:35.577000', 45, 2, 12, 12, NULL),
(56, 'English Grammar in Use', 'dormitorio ventana 1 1', '1986-01-01', '9505661517000', '2026-01-10 21:54:09.889000', 46, 2, 12, 12, NULL),
(57, 'Practical English Usage', 'dormitorio ventana 1 1', '1986-01-01', '0594311856000', '2026-01-10 22:13:11.672000', 47, 2, 17, 12, NULL),
(58, 'Lethal White', 'dormitorio ventana 1 1', '2018-09-01', '9780316422734', '2026-01-11 21:21:02.671000', 48, 2, 6, 6, NULL),
(59, 'Maria Antonieta Intima', 'dormitorio venta 1 2', '1908-01-01', NULL, '2026-01-13 20:21:56.565000', 49, 1, 28, NULL, NULL),
(60, 'Historia de la Ciencia de San Agustin a Galileo', 'dormitorio ventana 2', '1974-01-01', '8420620769000', '2026-01-13 20:47:08.284000', 50, 1, 29, 1, NULL),
(61, 'Historia de la España Musulmana', 'dormitorio venta 2', '1932-01-01', NULL, '2026-01-13 20:50:05.350000', 51, 1, 30, 1, NULL),
(62, 'Historia de Belgrano 1', 'dormitorio ventana 2', '1967-01-01', NULL, '2026-01-14 20:07:16.936000', 52, 1, 31, 1, NULL),
(63, 'Historia de Belgrano 2', 'dormitorio ventana 2', '1968-01-01', NULL, '2026-01-14 20:08:24.326000', 52, 1, 31, 1, NULL),
(64, 'Historia de Belgrano 3', 'dormitorio ventana 2', '1968-01-01', NULL, '2026-01-14 20:09:21.175000', 52, 1, 31, 1, NULL),
(65, 'Historia de Belgrano 4', 'dormitorio ventana 4', '1968-01-01', NULL, '2026-01-14 20:10:05.626000', 52, 1, 31, 1, NULL),
(66, 'La Cartuja de Parma', 'dormitorio ventana 2', '1946-10-04', NULL, '2026-01-14 20:13:04.699000', 53, 1, 4, 6, NULL),
(68, 'Don Tristan de Leonis', 'dormitorio ventana 2', '1953-08-18', NULL, '2026-01-14 20:21:26.565000', 56, 1, 33, 6, NULL),
(69, 'Cuentos de la Alhambra', 'dormitorio ventana 2', '1951-01-01', NULL, '2026-01-14 20:46:07.699000', 57, 1, 55, 1, NULL),
(71, 'Las Pobres Gentes', 'dormitorio ventana 2', '1945-05-03', NULL, '2026-01-14 21:13:31.236000', 61, 1, 4, 6, NULL),
(72, 'Wes African Explores', 'dormitorio ventana 2', '1955-01-01', NULL, '2026-01-14 21:17:29.951000', 62, 2, 35, 1, NULL),
(73, 'Cien Cuentos Populares Españoles', 'dormitorio ventana 2', '1942-01-01', NULL, '2026-01-14 21:23:00.985000', 63, 1, 36, 10, NULL),
(74, 'Los Griegos', 'dormitorio ventana 2', '1977-01-01', NULL, '2026-01-14 21:26:10.820000', 64, 1, 37, 1, NULL),
(76, 'El Candor del Padre Brown', 'dormitorio ventana 2', '1971-01-01', NULL, '2026-01-14 21:33:38.504000', 66, 1, 54, 6, NULL),
(77, 'English Vocabulary in Use', 'dormitorio ventana 2', NULL, '0521423961000', '2026-01-15 18:21:07.433000', 67, 2, 40, 13, NULL),
(78, 'Cuentas Cifradas', 'dormitorio ventana 2', '1983-01-01', '8432078573000', '2026-01-15 18:28:58.730000', 68, 1, 42, 4, NULL),
(79, 'Diccionario de Sinónimos y Antónimos', 'dormitorio ventana 2', '1999-01-01', NULL, '2026-01-15 18:35:16.828000', 69, 1, 43, 12, NULL),
(80, 'El Horroroso Crimen de Peñaranda del Campo', 'dormitorio ventana 2', '1928-01-01', NULL, '2026-01-15 18:39:15.279000', 70, 1, 44, 6, NULL),
(81, 'Las Noches del Cafe de Alzate', 'dormitorio ventana 2', '1928-01-01', NULL, '2026-01-15 18:41:24.057000', 70, 1, 44, 8, NULL),
(82, 'La Esvastica de Oro', 'dormitorio ventana 2', '1928-01-01', NULL, '2026-01-15 20:32:02.077000', 70, 1, 44, 8, NULL),
(83, 'San Martin y la Tercera Invasion Inglesa', 'dormitorio ventana 2', '1997-01-01', '9507861491000', '2026-01-15 20:35:01.165000', 71, 1, 12, 3, NULL),
(84, 'El Adereso de Brillantes', 'dormitorio ventana 2', '1975-01-01', NULL, '2026-01-15 20:38:56.737000', 72, 1, 57, 15, NULL),
(85, 'Don Quijote de la Mancha', 'dormitorio ventana 2', '1951-11-03', NULL, '2026-01-15 20:44:11.952000', 73, 1, 47, 6, NULL),
(86, 'Nuestro Hombre en La Havana', 'dormitorio ventana 2', '1959-04-14', NULL, '2026-01-15 20:46:40.428000', 5, 1, 4, 6, NULL),
(87, 'El Factor Humano', 'dormitorio ventana 2', '1979-05-01', NULL, '2026-01-15 20:48:02.759000', 5, 1, 4, 6, NULL),
(88, 'Historia de una Cobardía', 'dormitorio ventana 2', '1965-01-01', NULL, '2026-01-15 20:49:07.161000', 5, 1, 4, 6, '2026-02-05 21:29:22.476867'),
(89, 'El POder y la Gloria', 'dormitorio ventana 2', '1952-10-01', NULL, '2026-01-15 20:50:03.076000', 5, 1, 4, 6, NULL),
(91, 'El Escalpelo de Scotland Yard', 'dormitorio ventana 2', '1955-01-01', NULL, '2026-01-15 21:01:52.589000', 79, 1, 58, 1, NULL),
(92, 'Historia de la Ciudad de Mexico', 'dormitorio ventana 2', '1946-01-01', NULL, '2026-01-15 21:06:44.167000', 80, 1, 50, 1, NULL),
(93, 'Homosexualismo Creador', 'dormitorio ventana 2', '1932-01-01', NULL, '2026-01-15 21:10:52.194000', 8, 1, 51, 13, NULL),
(94, 'Sodoma y Gomorra', 'dormitorio ventana 2', '1645-09-04', NULL, '2026-01-15 21:16:01.741000', 81, 1, 52, 1, NULL),
(95, 'Las Estrellas Miran hacia Abajo', 'dormitorio ventana 2', '1945-03-16', NULL, '2026-01-15 21:19:13.506000', 82, 1, 53, 6, NULL),
(96, 'Diccionario Ideológico de la Lengua Española', 'dormitorio ventana 2', '1948-01-01', NULL, '2026-01-15 21:24:05.254000', 83, 1, 54, 12, NULL),
(97, 'Los Hebreos', 'dormitorio puerta', '1991-04-01', '9509495271', '2026-01-29 19:00:37.480544', 84, 1, 59, 1, '2026-01-29 19:04:21.613998'),
(98, 'Introduccion a la Filosofia', 'dormitorio puerta', '1959-03-01', NULL, '2026-01-29 19:26:16.774139', 85, 1, 60, 2, '2026-01-29 19:26:16.774148'),
(99, 'Tradiciones Peruanas', 'dormitorio puerta', '1953-01-01', NULL, '2026-01-29 19:29:05.174423', 86, 1, 61, 10, '2026-01-29 19:29:05.174433'),
(100, 'Historia de la Conquista de Mexico', 'dormitorio puerta', '1943-01-01', NULL, '2026-01-29 20:42:36.233032', 87, 1, 50, 1, '2026-01-29 20:42:36.233042'),
(101, 'Madame Bovary', 'dormitorio puerta', '1935-01-01', NULL, '2026-01-29 20:45:36.597428', 88, 1, 63, 6, '2026-01-29 20:45:36.597438'),
(102, 'Por Una Nueva Argentina', 'dormitorio puerta', '1940-01-01', NULL, '2026-01-29 20:52:19.035194', 89, 1, 64, 17, '2026-01-29 20:52:19.035203'),
(103, 'Gil Blas de Santillana', 'dormitorio puerta', '1973-01-01', NULL, '2026-01-29 20:56:12.417371', 90, 1, 65, 6, '2026-01-29 20:56:12.417380'),
(104, 'Los Tres Mosqueteros', 'dormitorio puerta', '1990-01-01', '8471130793', '2026-01-29 21:59:32.111431', 91, 1, 66, 6, '2026-01-29 21:59:32.111441'),
(105, 'El Libro de la Tranquilidad', 'dormitorio puerta', '2003-06-01', '9500719428', '2026-01-29 22:10:32.849287', 92, 1, 2, 18, '2026-01-29 23:03:05.872425'),
(106, 'Babel y el Castellano', 'dormitorio puerta', '1929-01-01', NULL, '2026-01-29 22:19:01.640687', 93, 1, 67, 9, '2026-01-29 22:19:01.640697'),
(107, 'El General Soler', 'dormitorio puerta', '1909-01-01', NULL, '2026-01-29 22:22:45.925419', 94, 1, 2, 1, '2026-01-29 22:22:45.925428'),
(108, 'Hernan Cortes', 'dormitorio puerta', '1941-01-01', NULL, '2026-01-29 22:50:01.464192', 95, 1, 68, 1, '2026-01-29 22:50:01.464202'),
(109, 'El Burgues', 'dormitorio puerta', '1977-01-01', '8420620270', '2026-01-29 22:59:24.495606', 96, 1, 29, 1, '2026-01-29 22:59:24.495615'),
(110, 'Recopilacion de Voces del Lunfardo', 'dormitorio puerta', '1980-09-01', NULL, '2026-01-30 19:33:01.370172', 97, 1, 69, 19, '2026-01-30 19:33:01.370183'),
(111, 'La Historia Secreta de la Historia', 'dormitorio puerta', '1983-12-07', '9500804034', '2026-01-30 19:36:20.641278', 98, 1, 70, 1, '2026-01-30 19:36:20.641288'),
(112, 'Novelas de Intriga', 'dormitorio puerta', '1961-01-01', NULL, '2026-01-30 19:39:29.916516', 99, 1, 61, 6, '2026-01-30 19:39:29.916525'),
(113, 'Madame Bovary', 'dormitorio puerta', '1982-01-01', '9506140022', '2026-01-30 19:42:21.324046', 88, 1, 71, 6, '2026-01-30 19:47:02.841669'),
(114, 'La Antorcha Eterna', 'dormitorio puerta', '1957-01-01', NULL, '2026-01-30 19:44:35.740184', 82, 1, 72, 6, '2026-01-30 19:44:35.740194'),
(115, 'Vinas de Ira', 'dormitorio puerta', '1940-01-01', NULL, '2026-01-31 20:04:23.629469', 100, 1, 53, 6, '2026-01-31 20:04:23.629478'),
(116, 'Novelas de Aventuras', 'dormitorio puerta', '1964-01-01', NULL, '2026-01-31 21:10:46.797647', 101, 1, 61, 6, '2026-01-31 21:10:46.797657'),
(117, 'Mis Suspenses Favoritas', 'dormitorio puerta', '1964-01-01', NULL, '2026-01-31 21:15:16.188180', 102, 1, 61, 6, '2026-01-31 21:15:16.188190'),
(118, 'Don Segundo Sombra', 'dormitorio puerta', '1952-01-01', NULL, '2026-01-31 21:21:03.991564', 103, 1, 74, 1, '2026-01-31 21:22:14.812921'),
(119, 'El Orinoco', 'dormitorio puerta', '1950-01-01', NULL, '2026-01-31 21:29:19.504833', 104, 1, 61, 1, '2026-01-31 21:29:19.504844'),
(120, 'Teoria Microeconomica', 'dormitorio puerta', '1980-01-01', '9681602765', '2026-01-31 21:33:15.190102', 105, 1, 7, 4, '2026-01-31 21:33:15.190111'),
(121, 'Tablas Estadísticas', 'dormitorio puerta', '1975-09-01', NULL, '2026-01-31 21:35:55.037842', 106, 1, 67, 16, '2026-01-31 21:35:55.037852'),
(122, 'Costos Bancarios', 'dormitorio puerta', '1983-09-01', '9505370409', '2026-02-01 18:37:16.007540', 107, 1, 75, 16, '2026-02-01 18:37:16.007550'),
(123, 'Tecnicas de Negociaciones', 'dormitorio puerta', '1987-01-01', '8585037121', '2026-02-01 18:41:58.104134', 108, 1, 76, 16, '2026-02-01 18:41:58.104144'),
(124, 'Historia Argentina', 'dormitorio puerta', '1969-03-20', NULL, '2026-02-01 18:45:12.353150', 109, 1, 77, 1, '2026-02-01 18:45:12.353166'),
(125, 'Ensayos sobre Teoria Contable', 'dormitorio puerta', '1975-01-01', NULL, '2026-02-01 18:50:16.103256', 110, 1, 75, 17, '2026-02-01 18:50:16.103265'),
(126, 'Los Indicadores Economicos', 'dormitorio puerta', '1977-05-01', NULL, '2026-02-01 18:53:34.618026', 111, 1, 75, 4, '2026-02-01 18:53:34.618036'),
(127, 'El Ajuste Estados Contables por Inflacion', 'dormitorio puerta', '1976-09-01', NULL, '2026-02-01 19:00:10.454807', 112, 1, 78, 16, '2026-02-01 19:00:10.454817'),
(128, 'Costos Bancarios', '', NULL, NULL, '2026-02-01 19:24:53.173702', 4, NULL, 12, NULL, '2026-02-01 19:24:53.173721'),
(129, 'El Escarmiento', 'biblioteca individual', NULL, '9789500732246', '2026-04-25 21:32:41.338855', 113, 1, 2, 3, '2026-04-25 21:32:41.338855'),
(130, 'Volver a Matar', 'Biblioteca individual', NULL, '9789500730686', '2026-04-25 21:33:55.104659', 113, 1, 2, 3, '2026-04-25 21:33:55.104659'),
(131, 'El Relato Peronista', 'Biblioteca indivisual', NULL, '9789509945567', '2026-04-25 21:48:42.551178', 114, 1, 47, 3, '2026-04-25 21:48:42.551178'),
(132, 'El Inventor del Peronismo', 'Biblioteca individual', NULL, '9789504931614', '2026-04-25 21:51:22.088123', 114, 1, 79, 3, '2026-04-25 21:55:56.205529'),
(133, 'Operación Traviata', 'Biblioteca individual', NULL, '9789500729581', '2026-04-25 21:58:25.373215', 113, 1, 2, 3, '2026-04-25 21:58:25.373215'),
(134, 'Disposicion Final', 'Biblioteca individual', NULL, '9789500754699', '2026-04-25 22:01:44.695581', 115, 1, 2, 3, '2026-04-25 22:01:44.695581'),
(135, 'Codigo Stiuso', 'Biblioteca individual estante 1', NULL, '9789504943952', '2026-04-25 22:09:31.120248', 116, 1, 79, 3, '2026-04-27 22:14:10.537253'),
(136, 'Los Intocables', 'Biblioteca individual', NULL, '9507427422', '2026-04-26 21:19:33.348310', 117, 1, 79, 3, '2026-04-26 21:19:33.348310'),
(137, 'Los Dueños de la Argentina', 'Biblioteca individual', NULL, '9500707462', '2026-04-26 21:22:12.910524', 118, 1, 2, 3, '2026-04-26 21:22:12.910524'),
(138, 'El malestar de la politica', 'Biblioteca individual', NULL, '9789500740418', '2026-04-26 21:33:36.143520', 119, 1, 2, 3, '2026-04-26 21:33:36.143520'),
(139, 'El Corralito Populista', 'Biblioteca individual', NULL, '9789500430296', '2026-04-26 21:38:59.028391', 120, 1, 4, 3, '2026-04-26 21:38:59.028391'),
(140, 'La Audacia y el calculo', 'Biblioteca individual', NULL, '9789500735049', '2026-04-26 21:44:17.702618', 121, 1, 2, 3, '2026-04-26 21:44:17.703624'),
(141, 'Aerolineas Argentinas', 'Biblioteca individual', NULL, '9789504941866', '2026-04-26 22:05:58.280979', 122, 1, 79, 3, '2026-04-26 22:05:58.281978'),
(142, 'Argentinos', 'Biblioteca individual', NULL, '9500152258', '2026-04-26 22:12:50.636567', 123, 1, 10, 3, '2026-04-26 22:12:50.636567'),
(143, 'La Corrupcion', 'Biblioteca individual', NULL, '9507423265', '2026-04-26 22:15:37.412407', 124, 1, 79, 3, '2026-04-26 22:15:37.412407'),
(144, 'Enemigos Publicos', 'Biblioteca individual', NULL, '9505118104', '2026-04-26 22:24:57.789332', 125, 1, 61, 3, '2026-04-26 22:24:57.789332'),
(145, 'San Martin', 'Biblioteca individual estante 1', NULL, '9789500739597', '2026-04-27 21:33:19.112263', 126, 1, 2, 1, '2026-04-27 21:39:38.701308'),
(146, 'Breve Historia de los Argentinos', 'Biblioteca individual estante 1', NULL, '9507424156', '2026-04-27 21:35:08.471182', 3, 1, 79, 1, '2026-04-27 21:35:08.471182'),
(147, 'Heroes', 'Biblioteca individual estante 1', NULL, '9788466623148', '2026-04-27 21:41:15.785118', 127, 1, 80, 1, '2026-04-27 21:42:21.838134'),
(148, 'Porque Crecen los Países', 'Biblioteca individual estante 1', NULL, '9789875662643', '2026-04-27 21:46:14.945438', 128, 1, 81, 1, '2026-04-27 21:46:14.945438'),
(149, 'Soy Roca', 'Bibliotyeca individual estante 2', NULL, '8448706145', '2026-04-27 21:48:23.968242', 3, 1, 29, 1, '2026-04-27 21:48:23.968242'),
(150, 'El Elogio de la Culpa', 'Biblioteca individual estante 2', NULL, '9507424148', '2026-04-27 22:06:02.447206', 129, 1, 79, 2, '2026-04-27 22:06:02.447206'),
(151, 'El Capital', 'Biblioteca individual estante 2', NULL, NULL, '2026-04-27 22:11:04.095884', 130, 1, 12, 4, '2026-04-27 22:11:04.095884'),
(152, 'Aprender a curarse', 'Biblioteca individual 3 est', '1992-10-24', '9504333150', '2026-05-01 21:48:26.864533', 131, 1, 82, 20, '2026-05-01 21:49:54.559873'),
(153, 'El Doble', 'Biblioteca individual est 3', '1996-09-28', '0812817311', '2026-05-02 19:54:49.608100', 132, 1, 83, 6, '2026-05-02 19:59:01.720788'),
(154, 'El Hombre del Corazón Caído', 'Biblioteca individual est 3', '1990-05-01', '9506330093', '2026-05-02 20:15:53.019863', 134, 1, 12, 6, '2026-05-02 20:15:53.020899'),
(155, 'Un dia en la vida de Iván Denisovich', 'Biblioteca individual est 3', '1983-10-15', '8449966450', '2026-05-02 20:24:04.112030', 135, 1, 71, 11, '2026-05-02 20:24:04.112030'),
(156, 'El Hambre', 'Biblioteca individual est 3', '2014-08-01', '9789504940531', '2026-05-02 20:27:31.009039', 136, 1, 79, 17, '2026-05-02 20:27:31.009039'),
(157, 'Memorias', 'Biblioteca individual est 3', '1977-05-01', NULL, '2026-05-02 21:35:20.946078', 137, 1, 21, 11, '2026-05-02 21:35:20.946078'),
(158, 'Eugenia Grandet', 'Biblioteca individual est 3', '1978-01-01', '8402054943', '2026-05-02 21:44:31.410796', 138, 1, 70, 11, '2026-05-02 21:44:31.410796'),
(159, 'Degenerado', 'Biblioteca individual 3 est', '2019-06-01', '9788733998998', '2026-05-02 22:09:16.959958', 139, 1, 84, 11, '2026-05-02 22:11:17.355142');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `core_user`
--

CREATE TABLE `core_user` (
  `id` bigint NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `email` varchar(254) NOT NULL,
  `avatar` varchar(100) DEFAULT NULL,
  `bio` longtext,
  `role` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `core_user`
--

INSERT INTO `core_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `is_staff`, `is_active`, `date_joined`, `email`, `avatar`, `bio`, `role`) VALUES
(1, 'pbkdf2_sha256$1200000$x6g73N6RB2cLXnA2EcrYzv$E2FSWlokpz2HINUfFMYIgPLBXkdiEGANv/GlaevEYho=', '2026-05-02 19:49:34.801371', 1, 'daniel', '', '', 1, 1, '2025-12-22 20:13:51.254000', 'daniel1713@gmail.com', '', NULL, 'viewer');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `core_user_groups`
--

CREATE TABLE `core_user_groups` (
  `id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  `group_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `core_user_user_permissions`
--

CREATE TABLE `core_user_user_permissions` (
  `id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  `permission_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint UNSIGNED NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` bigint NOT NULL
) ;

--
-- Volcado de datos para la tabla `django_admin_log`
--

INSERT INTO `django_admin_log` (`id`, `action_time`, `object_id`, `object_repr`, `action_flag`, `change_message`, `content_type_id`, `user_id`) VALUES
(1, '2025-12-22 20:56:35.332000', '1', 'Argentina', 1, '[{\"added\": {}}]', 7, 1),
(2, '2025-12-22 20:56:50.672000', '2', 'Ingles', 1, '[{\"added\": {}}]', 7, 1),
(3, '2025-12-22 20:57:00.540000', '3', 'Frances', 1, '[{\"added\": {}}]', 7, 1),
(4, '2025-12-22 21:32:21.883000', '1', 'Español', 1, '[{\"added\": {}}]', 28, 1),
(5, '2025-12-22 21:32:55.957000', '2', 'Ingles', 1, '[{\"added\": {}}]', 28, 1),
(6, '2025-12-22 21:33:04.755000', '2', 'Ingles', 2, '[]', 28, 1),
(7, '2025-12-22 21:33:16.036000', '3', 'Frances', 1, '[{\"added\": {}}]', 28, 1),
(8, '2025-12-22 21:33:22.772000', '4', 'Aleman', 1, '[{\"added\": {}}]', 28, 1),
(9, '2025-12-22 21:33:30.097000', '5', 'Japones', 1, '[{\"added\": {}}]', 28, 1),
(10, '2025-12-22 21:34:00.709000', '1', 'Historia', 1, '[{\"added\": {}}]', 10, 1),
(11, '2025-12-22 21:34:20.156000', '2', 'Filosofia', 1, '[{\"added\": {}}]', 10, 1),
(12, '2025-12-22 21:34:49.594000', '3', 'Politica', 1, '[{\"added\": {}}]', 10, 1),
(13, '2025-12-22 21:35:03.731000', '4', 'Economia', 1, '[{\"added\": {}}]', 10, 1),
(14, '2025-12-22 21:37:05.321000', '5', 'Legislacion', 1, '[{\"added\": {}}]', 10, 1),
(15, '2025-12-23 18:14:30.643000', '4', 'Español', 1, '[{\"added\": {}}]', 7, 1),
(16, '2025-12-23 18:18:57.576000', '5', 'Colombia', 1, '[{\"added\": {}}]', 7, 1),
(17, '2025-12-27 18:43:15.926000', '4', 'Aleman', 3, '', 28, 1),
(18, '2025-12-27 18:43:30.882000', '6', 'Aleman', 1, '[{\"added\": {}}]', 28, 1),
(19, '2025-12-27 18:44:04.108000', '6', 'Aleman', 1, '[{\"added\": {}}]', 7, 1),
(20, '2025-12-27 19:18:18.402000', '7', 'Dinamarca', 1, '[{\"added\": {}}]', 7, 1),
(21, '2025-12-27 19:18:27.296000', '8', 'Suecia', 1, '[{\"added\": {}}]', 7, 1),
(22, '2025-12-27 19:18:37.331000', '9', 'Noruega', 1, '[{\"added\": {}}]', 7, 1),
(23, '2025-12-27 19:19:04.665000', '10', 'Rusia', 1, '[{\"added\": {}}]', 7, 1),
(24, '2025-12-27 19:19:30.345000', '11', 'Hungria', 1, '[{\"added\": {}}]', 7, 1),
(25, '2025-12-27 19:19:42.902000', '12', 'Polonia', 1, '[{\"added\": {}}]', 7, 1),
(26, '2025-12-27 19:19:53.818000', '13', 'Estonia', 1, '[{\"added\": {}}]', 7, 1),
(27, '2025-12-27 19:20:02.708000', '14', 'Lituania', 1, '[{\"added\": {}}]', 7, 1),
(28, '2025-12-27 19:20:21.834000', '15', 'Eslovenia', 1, '[{\"added\": {}}]', 7, 1),
(29, '2025-12-27 19:20:41.533000', '16', 'Italia', 1, '[{\"added\": {}}]', 7, 1),
(30, '2025-12-27 19:20:55.102000', '17', 'Grecia', 1, '[{\"added\": {}}]', 7, 1),
(31, '2025-12-27 19:21:51.494000', '6', 'Alemania', 2, '[{\"changed\": {\"fields\": [\"Name\"]}}]', 7, 1),
(32, '2025-12-27 19:22:21.685000', '3', 'Francia', 2, '[{\"changed\": {\"fields\": [\"Name\"]}}]', 7, 1),
(33, '2025-12-27 19:22:37.102000', '2', 'Inglaterra', 2, '[{\"changed\": {\"fields\": [\"Name\"]}}]', 7, 1),
(34, '2025-12-28 20:41:41.166000', '18', 'Estados Unidos', 1, '[{\"added\": {}}]', 7, 1),
(35, '2025-12-28 20:41:56.115000', '4', 'España', 2, '[{\"changed\": {\"fields\": [\"Name\"]}}]', 7, 1),
(36, '2025-12-28 20:42:21.920000', '19', 'Brazil', 1, '[{\"added\": {}}]', 7, 1),
(37, '2025-12-28 20:42:38.819000', '20', 'Chile', 1, '[{\"added\": {}}]', 7, 1),
(38, '2025-12-28 20:42:53.871000', '21', 'Peru', 1, '[{\"added\": {}}]', 7, 1),
(39, '2025-12-28 20:43:19.294000', '22', 'Mexico', 1, '[{\"added\": {}}]', 7, 1),
(40, '2025-12-29 19:31:07.741000', '23', 'Irlanda', 1, '[{\"added\": {}}]', 7, 1),
(41, '2025-12-31 22:07:39.703000', '24', 'Escocia', 1, '[{\"added\": {}}]', 7, 1),
(42, '2026-01-13 20:44:34.568000', '25', 'Australia', 1, '[{\"added\": {}}]', 7, 1),
(43, '2026-02-05 21:29:22.479705', '88', 'Historia de una Cobardía (Greene)', 2, '[]', 8, 1),
(44, '2026-05-02 19:55:51.396460', '26', 'Turquia', 1, '[{\"added\": {}}]', 7, 1),
(45, '2026-05-02 19:57:03.826743', '83', 'Editorial Vergara', 1, '[{\"added\": {}}]', 9, 1),
(46, '2026-05-02 22:10:11.185958', '84', 'Anagrama Editorial', 1, '[{\"added\": {}}]', 9, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(2, 'auth', 'group'),
(3, 'auth', 'permission'),
(6, 'authors', 'author'),
(7, 'authors', 'nationality'),
(8, 'books', 'book'),
(28, 'books', 'language'),
(4, 'contenttypes', 'contenttype'),
(13, 'core', 'user'),
(11, 'language', 'language'),
(9, 'publishing_houses', 'publishinghouse'),
(12, 'search', 'search'),
(5, 'sessions', 'session'),
(10, 'themes', 'theme');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2026-01-20 21:41:27.976051'),
(2, 'contenttypes', '0002_remove_content_type_name', '2026-01-20 21:41:28.056156'),
(3, 'auth', '0001_initial', '2026-01-20 21:41:28.304252'),
(4, 'auth', '0002_alter_permission_name_max_length', '2026-01-20 21:41:28.372101'),
(5, 'auth', '0003_alter_user_email_max_length', '2026-01-20 21:41:28.376855'),
(6, 'auth', '0004_alter_user_username_opts', '2026-01-20 21:41:28.381294'),
(7, 'auth', '0005_alter_user_last_login_null', '2026-01-20 21:41:28.385905'),
(8, 'auth', '0006_require_contenttypes_0002', '2026-01-20 21:41:28.388915'),
(9, 'auth', '0007_alter_validators_add_error_messages', '2026-01-20 21:41:28.393880'),
(10, 'auth', '0008_alter_user_username_max_length', '2026-01-20 21:41:28.400991'),
(11, 'auth', '0009_alter_user_last_name_max_length', '2026-01-20 21:41:28.406039'),
(12, 'auth', '0010_alter_group_name_max_length', '2026-01-20 21:41:28.420572'),
(13, 'auth', '0011_update_proxy_permissions', '2026-01-20 21:41:28.425986'),
(14, 'auth', '0012_alter_user_first_name_max_length', '2026-01-20 21:41:28.431766'),
(15, 'core', '0001_initial', '2026-01-20 21:41:28.900740'),
(16, 'admin', '0001_initial', '2026-01-20 21:41:29.045942'),
(17, 'admin', '0002_logentry_remove_auto_add', '2026-01-20 21:41:29.052857'),
(18, 'admin', '0003_logentry_add_action_flag_choices', '2026-01-20 21:41:29.059906'),
(19, 'themes', '0001_initial', '2026-01-20 21:41:29.145418'),
(20, 'publishing_houses', '0001_initial', '2026-01-20 21:41:29.216489'),
(21, 'books', '0001_initial', '2026-01-20 21:41:29.235470'),
(22, 'authors', '0001_initial', '2026-01-20 21:41:29.260663'),
(23, 'authors', '0002_initial', '2026-01-20 21:41:29.319204'),
(24, 'authors', '0003_author', '2026-01-20 21:41:29.340890'),
(25, 'books', '0002_book', '2026-01-20 21:41:29.471477'),
(26, 'books', '0003_book_publishing_houses_book_theme', '2026-01-20 21:41:29.620019'),
(27, 'books', '0004_delete_book', '2026-01-20 21:41:29.642150'),
(28, 'authors', '0004_author_created_by_author_nationality', '2026-01-20 21:41:29.754220'),
(29, 'authors', '0005_delete_author', '2026-01-20 21:41:29.774290'),
(30, 'authors', '0006_author', '2026-01-20 21:41:29.906734'),
(31, 'authors', '0007_alter_author_options_alter_nationality_options', '2026-01-20 21:41:29.918302'),
(32, 'language', '0001_initial', '2026-01-20 21:41:29.938940'),
(33, 'books', '0005_book', '2026-01-20 21:41:30.250721'),
(34, 'books', '0006_alter_book_language_and_more', '2026-01-20 21:41:30.737126'),
(35, 'search', '0001_initial', '2026-01-20 21:41:30.758772'),
(36, 'sessions', '0001_initial', '2026-01-20 21:41:30.802410'),
(37, 'books', '0007_alter_book_updated_at', '2026-01-24 20:47:13.776736'),
(38, 'authors', '0008_alter_author_updated_at', '2026-01-24 21:11:52.333693'),
(39, 'publishing_houses', '0002_publishinghouse_updated_at', '2026-01-24 21:11:52.377975'),
(40, 'themes', '0002_theme_updated_at', '2026-01-24 21:11:52.441343'),
(41, 'authors', '0009_alter_author_last_name', '2026-01-29 21:33:58.558339'),
(42, 'language', '0002_alter_language_options_alter_language_name', '2026-01-29 21:33:58.596187'),
(43, 'publishing_houses', '0003_alter_publishinghouse_name', '2026-01-29 21:33:58.644266'),
(44, 'themes', '0003_alter_theme_options', '2026-01-29 21:33:58.655264'),
(45, 'authors', '0010_alter_author_last_name', '2026-05-02 20:15:25.988628');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('0w74q0pirbvarjtek4bkmzupsicoy85z', '.eJxVjMsOwiAQRf-FtSHDo1BcuvcbyAwMUjU0Ke3K-O_apAvd3nPOfYmI21rj1nmJUxZnocTpdyNMD247yHdst1mmua3LRHJX5EG7vM6Zn5fD_Tuo2Ou3NlyKH4gdACmvDWlnHARM2gYk6x06Mw4hjeA1qKRTYQgOswVL6I0S7w_Ptjcu:1wHTVI:tyNUbgRCkZO34gXXRM5Nfc5bWv74n2hSCUHj-hhEUDA', '2026-05-11 21:28:32.131079'),
('6diges4kmjw6axqmidkp1d8i9quz4lbi', '.eJxVjMsOwiAQRf-FtSHDo1BcuvcbyAwMUjU0Ke3K-O_apAvd3nPOfYmI21rj1nmJUxZnocTpdyNMD247yHdst1mmua3LRHJX5EG7vM6Zn5fD_Tuo2Ou3NlyKH4gdACmvDWlnHARM2gYk6x06Mw4hjeA1qKRTYQgOswVL6I0S7w_Ptjcu:1wH6qA:dslbDDQv8fpV-qd4A9fJRL9gdLDOEScf8PbwmrJEm48', '2026-05-10 21:16:34.909935'),
('ccnzzbblb52lewvh9s7rsqfyrs38ny9k', '.eJxVjMsOwiAQRf-FtSHDo1BcuvcbyAwMUjU0Ke3K-O_apAvd3nPOfYmI21rj1nmJUxZnocTpdyNMD247yHdst1mmua3LRHJX5EG7vM6Zn5fD_Tuo2Ou3NlyKH4gdACmvDWlnHARM2gYk6x06Mw4hjeA1qKRTYQgOswVL6I0S7w_Ptjcu:1vjlMx:uKL7IW3YDMQk28YDhYXrTpzY0mUNPJYZl1u8ZE3xxrs', '2026-02-07 21:40:35.140503'),
('hhb920xy86h9dzxawmuc8944iieopxjy', 'e30:1vidAb:X5JJOIm85PcN2KEiU2k83KnhnCwDTEPbs79I_rs7s7E', '2026-02-04 18:43:09.821984'),
('nrrhtdp0lrqswlw08tst5xkfirc0zuer', '.eJxVjMsOwiAQRf-FtSHDo1BcuvcbyAwMUjU0Ke3K-O_apAvd3nPOfYmI21rj1nmJUxZnocTpdyNMD247yHdst1mmua3LRHJX5EG7vM6Zn5fD_Tuo2Ou3NlyKH4gdACmvDWlnHARM2gYk6x06Mw4hjeA1qKRTYQgOswVL6I0S7w_Ptjcu:1wJGLG:DXmqPGXH5kdBOHmgiYK4rJ8GQfEeTRPc6V8brl8pJYg', '2026-05-16 19:49:34.807330'),
('so4snz3l1w5lnjvpsesh8qbryj6h6vsd', '.eJxVjMsOwiAQRf-FtSHDo1BcuvcbyAwMUjU0Ke3K-O_apAvd3nPOfYmI21rj1nmJUxZnocTpdyNMD247yHdst1mmua3LRHJX5EG7vM6Zn5fD_Tuo2Ou3NlyKH4gdACmvDWlnHARM2gYk6x06Mw4hjeA1qKRTYQgOswVL6I0S7w_Ptjcu:1wIYMf:Q8j_r4hESwl1sYSr5Yj_t85cS07w8RTl-0w73aUIYgY', '2026-05-14 20:52:05.367792'),
('v4zoldo26io0tcstzanvv79ap2gmdnt0', '.eJxVjMsOwiAQRf-FtSHDo1BcuvcbyAwMUjU0Ke3K-O_apAvd3nPOfYmI21rj1nmJUxZnocTpdyNMD247yHdst1mmua3LRHJX5EG7vM6Zn5fD_Tuo2Ou3NlyKH4gdACmvDWlnHARM2gYk6x06Mw4hjeA1qKRTYQgOswVL6I0S7w_Ptjcu:1vp96V:AXSRhXF1ILXCyNR_ohlcPobViAnWipM6Hz4rEIwgMNg', '2026-02-22 18:01:51.068131'),
('wofduqdi67d7ttzmbzyubmdh8rj2aii2', '.eJxVjMsOwiAQRf-FtSHDo1BcuvcbyAwMUjU0Ke3K-O_apAvd3nPOfYmI21rj1nmJUxZnocTpdyNMD247yHdst1mmua3LRHJX5EG7vM6Zn5fD_Tuo2Ou3NlyKH4gdACmvDWlnHARM2gYk6x06Mw4hjeA1qKRTYQgOswVL6I0S7w_Ptjcu:1wGkQR:heuFUnBxCGRTbXdctLf3qyrLt6VkZl0iQrYF3QG2zs8', '2026-05-09 21:20:31.866535'),
('x7rsrf6vyd14vso28bg6n32oyw992ksy', '.eJxVjMEOwiAQBf-FsyGwlAU8evcbCLAgVQNJaU_Gf9cmPej1zcx7MR-2tfpt5MXPxM5MstPvFkN65LYDuod26zz1ti5z5LvCDzr4tVN-Xg7376CGUb91EVaCQ1FMSYAa3YTZSgKjFYGSVsVChgSpXLKT2glwARFE0XYCiZq9P7yiNpY:1vY4YO:07R-CdnO5U1VRyz7KuKNiFwv0rcdhS-2tzBa4o8e3M8', '2026-01-06 15:44:04.914000'),
('y73o6l6gadkod1i906jfj5u1ajwudz27', '.eJxVjMEOwiAQBf-FsyGwlAU8evcbCLAgVQNJaU_Gf9cmPej1zcx7MR-2tfpt5MXPxM5MstPvFkN65LYDuod26zz1ti5z5LvCDzr4tVN-Xg7376CGUb91EVaCQ1FMSYAa3YTZSgKjFYGSVsVChgSpXLKT2glwARFE0XYCiZq9P7yiNpY:1vdvVe:gRdPYSBcAcHTFsLbbkxlUpNkrNWUXffRpciRYTrO7cs', '2026-01-22 19:17:26.138000');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `language_language`
--

CREATE TABLE `language_language` (
  `id` bigint NOT NULL,
  `name` varchar(50) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) DEFAULT NULL,
  `created_by` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `language_language`
--

INSERT INTO `language_language` (`id`, `name`, `created_at`, `updated_at`, `created_by`) VALUES
(1, 'Español', '2025-12-22 21:32:21.882000', NULL, NULL),
(2, 'Ingles', '2025-12-22 21:32:55.956000', NULL, NULL),
(3, 'Frances', '2025-12-22 21:33:16.035000', NULL, NULL),
(5, 'Japones', '2025-12-22 21:33:30.096000', NULL, NULL),
(6, 'Aleman', '2025-12-27 18:43:30.882000', NULL, NULL),
(7, 'Danes', '2026-02-01 19:26:22.603505', '2026-02-01 19:26:22.603522', NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `publishing_houses_publishinghouse`
--

CREATE TABLE `publishing_houses_publishinghouse` (
  `id` bigint NOT NULL,
  `name` varchar(200) NOT NULL,
  `country` varchar(100) NOT NULL,
  `created_by_id` bigint DEFAULT NULL,
  `updated_at` datetime(6) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `publishing_houses_publishinghouse`
--

INSERT INTO `publishing_houses_publishinghouse` (`id`, `name`, `country`, `created_by_id`, `updated_at`) VALUES
(1, 'Penguin Popular Classics', 'Great Britain', 1, NULL),
(2, 'Editorial Sudamericana', 'Argentina', 1, '2026-01-29 19:11:25.880559'),
(3, 'Taurus', 'España', 1, NULL),
(4, 'Emece', 'Argentina', 1, NULL),
(5, 'Vicens bolsillo', 'España', 1, NULL),
(6, 'Hachette', 'Francia', 1, NULL),
(7, 'Fondo de Cultura Economica', 'Mexico', 1, NULL),
(8, 'Plaza y Janes', 'España', 1, NULL),
(9, 'Sur', 'Argentina', 1, NULL),
(10, 'Ediciones Acervo', 'España', 1, NULL),
(11, 'Editorial Israel', 'Argentina', 1, NULL),
(12, 'Acme Agency', 'Argentina', 1, NULL),
(13, 'Editorial Catolica', 'España', 1, NULL),
(14, 'The L. W. Singer Ltd', 'Estados Unidos', 1, NULL),
(15, 'Collins Clear-Type', 'Inglaterra', 1, NULL),
(16, 'Penguins Books', 'Inglaterra', 1, NULL),
(17, 'Pelikan Books', 'Inglaterra', 1, NULL),
(18, 'Unwim Brothers', 'Inglaterra', 1, NULL),
(19, 'Hodder and Staughton', 'Inglaterra', 1, NULL),
(20, 'Longman Fiction', 'Inglaterra', 1, NULL),
(21, 'Pan Books Ltd', 'Inglaterra', 1, NULL),
(22, 'M. Dent and sons', 'Inglaterra', 1, NULL),
(23, 'Longman Singapure', 'Singapure', 1, NULL),
(24, 'King Penguin Book', 'United Kingdon', 1, NULL),
(25, 'Wolfe Publishing Ltd', 'United Kingdon', 1, NULL),
(26, 'Collins', 'United Kingdon', 1, NULL),
(27, 'Longman Caribbean', 'Virgin Islands', 1, NULL),
(28, 'Montaner y Simon Editores', 'España', 1, NULL),
(29, 'Alianza Editorial', 'España', 1, NULL),
(30, 'Editorial Labor', 'España', 1, NULL),
(31, 'Editorial Universitaria', 'Argentina', 1, NULL),
(32, 'Editorial Difusión', 'España', 1, NULL),
(33, 'Espasa Calpe Argentina', 'Argentina', 1, NULL),
(34, 'Impresores Ciudad Lineal', 'España', 1, NULL),
(35, 'Oxford University', 'Inglaterra', 1, NULL),
(36, 'Editorial Saeta', 'España', 1, NULL),
(37, 'Eudeba', 'Argentina', 1, NULL),
(38, 'Ediciones Tirso', 'España', 1, NULL),
(39, 'G.P. Ediciones', 'España', 1, NULL),
(40, 'Cambridge University', 'Inglaterra', 1, NULL),
(41, 'Ediciones Mezquita At-Taudi', 'Argentina', 1, NULL),
(42, 'Hamish Hamilton', 'Inglaterra', 1, NULL),
(43, 'Ediciones Larousse', 'Argentina', 1, NULL),
(44, 'Rafael Caro Raggio', 'España', 1, NULL),
(45, 'Editorial Biblos', 'Argentina', 1, NULL),
(46, 'Libreria Editorial Goncourd', 'Argentina', 1, NULL),
(47, 'Editorial Estrada', 'Aargentina', 1, NULL),
(48, 'Ediciones Norma', 'Argentina', 1, NULL),
(49, 'Biografias Gondesa', 'España', 1, NULL),
(50, 'Editorial Pablo Robredo', 'Mexico', 1, NULL),
(51, 'Javier Morate Editor', 'España', 1, NULL),
(52, 'Santiago Rueda Editor', 'Agentina', 1, NULL),
(53, 'Editorial Claridad', 'Argentina', 1, NULL),
(54, 'Editorial Gustavo Gil', 'Mexico', 1, NULL),
(55, 'Editorial Padre Suarez', 'España', 1, NULL),
(57, 'Ediciones Goncourd', 'Francia', 1, NULL),
(58, 'Editorial Grijalbo', 'Mexico', 1, NULL),
(59, 'Editorial Distal', 'Argentina', 1, '2026-01-29 19:01:58.562017'),
(60, 'Club de Lectores', 'Argentina', 1, '2026-01-29 19:05:07.610151'),
(61, 'Aguilar Ediciones', 'España', 1, '2026-01-29 19:05:34.744029'),
(62, 'Editorial Pedro Robrero', 'Mexico', 1, '2026-01-29 19:06:17.894957'),
(63, 'Ediciones Ercilla', 'Chile', NULL, '2026-01-29 19:07:27.493067'),
(64, 'Talleres Graficos Porter Hnos', 'Argentina', 1, '2026-01-29 19:08:04.927563'),
(65, 'Editorial Porrua', 'Mexico', 1, '2026-01-29 19:09:25.810085'),
(66, 'Ediciones Moreton', 'España', 1, '2026-01-29 19:09:56.861296'),
(67, 'Editorial del Colegio', 'Argentina', 1, '2026-01-29 19:10:45.994697'),
(68, 'Ediciones Xochitl', 'Mexico', 1, '2026-01-29 19:12:15.845002'),
(69, 'Ediciones Corregidor', 'Argentina', 1, '2026-01-29 19:12:52.511598'),
(70, 'Editorial Atlantida', 'Argentina', 1, '2026-01-29 19:17:04.597618'),
(71, 'Ediciones Orbis Hyspamerica', 'Argentina', 1, '2026-01-29 19:20:13.439427'),
(72, 'Ediciones Jackson', 'Argentina', 1, '2026-01-29 19:21:31.428708'),
(73, 'Ediciones Orbis', 'Argentina', 1, '2026-01-30 19:45:48.421932'),
(74, 'Ediciones Allantay', 'Argentina', 1, '2026-01-31 21:21:32.928742'),
(75, 'Ediciones Macchi', 'Argentina', 1, '2026-01-31 21:23:14.244314'),
(76, 'Ph.D. Editora', 'Brazil', 1, '2026-01-31 21:23:46.694155'),
(77, 'Soler/Hachette', 'Argentina', 1, '2026-01-31 21:24:15.477055'),
(78, 'Ediciones Contabilidad Moderna', 'Argentina', 1, '2026-01-31 21:24:50.927344'),
(79, 'Editorial Planeta', 'Argentina', 1, '2026-04-25 21:53:39.752630'),
(80, 'Ediciones BSA', 'Argentina', 1, '2026-04-27 21:41:52.066739'),
(81, 'Ediciones de Bolsillo', 'Argentina', 1, '2026-04-27 21:43:15.881780'),
(82, 'Colegio Salesiano San Jose', 'Argentina', 1, '2026-05-01 21:49:09.422859'),
(83, 'Editorial Vergara', 'Argentina', 1, '2026-05-02 19:57:03.825744'),
(84, 'Anagrama Editorial', 'España', 1, '2026-05-02 22:10:11.185958');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `search_search`
--

CREATE TABLE `search_search` (
  `id` bigint NOT NULL,
  `query` varchar(255) NOT NULL,
  `created_at` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `themes_theme`
--

CREATE TABLE `themes_theme` (
  `id` bigint NOT NULL,
  `name` varchar(100) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `created_by_id` bigint DEFAULT NULL,
  `updated_at` datetime(6) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `themes_theme`
--

INSERT INTO `themes_theme` (`id`, `name`, `created_at`, `created_by_id`, `updated_at`) VALUES
(1, 'Historia', '2025-12-22 21:34:00.709000', 1, NULL),
(2, 'Filosofia', '2025-12-22 21:34:20.156000', 1, NULL),
(3, 'Politica', '2025-12-22 21:34:49.594000', 1, NULL),
(4, 'Economia', '2025-12-22 21:35:03.730000', 1, NULL),
(5, 'Legislacion', '2025-12-22 21:37:05.320000', 1, NULL),
(6, 'Novela', '2025-12-23 16:21:25.220000', 1, NULL),
(7, 'Religion', '2025-12-23 21:52:07.837000', 1, NULL),
(8, 'Teatro', '2025-12-23 21:52:26.563000', 1, NULL),
(9, 'Costumbrista', '2025-12-23 21:52:55.620000', 1, NULL),
(10, 'Tradicion', '2025-12-23 21:54:55.613000', 1, NULL),
(11, 'Ficcion', '2025-12-28 20:38:15.022000', 1, NULL),
(12, 'Diccionario', '2026-01-09 22:45:32.643000', 1, NULL),
(13, 'Enseñanza', '2026-01-11 19:43:28.741000', 1, NULL),
(14, 'Curso', '2026-01-11 19:43:44.190000', 1, NULL),
(15, 'Cuento', '2026-01-15 20:40:38.108000', 1, NULL),
(16, 'Contabilidad', '2026-01-27 21:00:32.698275', 1, '2026-01-27 21:00:32.698295'),
(17, 'Ensayo', '2026-01-29 20:46:08.622564', 1, '2026-01-29 20:46:08.622578'),
(18, 'Espiritualidad', '2026-01-29 23:01:58.718020', 1, '2026-01-29 23:01:58.718036'),
(19, 'Texto', '2026-01-30 19:30:42.005703', 1, '2026-01-30 19:30:42.005719'),
(20, 'Medicina', '2026-05-01 21:49:30.506488', 1, '2026-05-01 21:49:30.506488');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `authors_author`
--
ALTER TABLE `authors_author`
  ADD PRIMARY KEY (`id`),
  ADD KEY `authors_author_created_by_id_9275319a_fk_core_user_id` (`created_by_id`),
  ADD KEY `authors_author_nationality_id_f5145aac_fk_authors_nationality_id` (`nationality_id`);

--
-- Indices de la tabla `authors_nationality`
--
ALTER TABLE `authors_nationality`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`),
  ADD KEY `authors_nationality_created_by_id_a9ad8ef4_fk_core_user_id` (`created_by_id`);

--
-- Indices de la tabla `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indices de la tabla `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Indices de la tabla `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Indices de la tabla `books_book`
--
ALTER TABLE `books_book`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `isbn` (`isbn`),
  ADD KEY `books_book_author_id_8b91747b_fk_authors_author_id` (`author_id`),
  ADD KEY `books_book_theme_id_6b0b49c2_fk_themes_theme_id` (`theme_id`),
  ADD KEY `books_book_language_id_b9f55b1a_fk_language_language_id` (`language_id`),
  ADD KEY `books_book_publishing_house_id_8e10b8c7_fk_publishin` (`publishing_house_id`),
  ADD KEY `books_book_title_d3218d_idx` (`title`),
  ADD KEY `books_book_isbn_54becd_idx` (`isbn`),
  ADD KEY `books_book_publica_4f381a_idx` (`publication_date`);

--
-- Indices de la tabla `core_user`
--
ALTER TABLE `core_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indices de la tabla `core_user_groups`
--
ALTER TABLE `core_user_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `core_user_groups_user_id_group_id_c82fcad1_uniq` (`user_id`,`group_id`),
  ADD KEY `core_user_groups_group_id_fe8c697f_fk_auth_group_id` (`group_id`);

--
-- Indices de la tabla `core_user_user_permissions`
--
ALTER TABLE `core_user_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `core_user_user_permissions_user_id_permission_id_73ea0daa_uniq` (`user_id`,`permission_id`),
  ADD KEY `core_user_user_permi_permission_id_35ccf601_fk_auth_perm` (`permission_id`);

--
-- Indices de la tabla `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_core_user_id` (`user_id`);

--
-- Indices de la tabla `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Indices de la tabla `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- Indices de la tabla `language_language`
--
ALTER TABLE `language_language`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `language_language_name_c2663efd_uniq` (`name`);

--
-- Indices de la tabla `publishing_houses_publishinghouse`
--
ALTER TABLE `publishing_houses_publishinghouse`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `publishing_houses_publishinghouse_name_295c1b06_uniq` (`name`),
  ADD KEY `publishing_houses_pu_created_by_id_4da9abaf_fk_core_user` (`created_by_id`);

--
-- Indices de la tabla `search_search`
--
ALTER TABLE `search_search`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `themes_theme`
--
ALTER TABLE `themes_theme`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`),
  ADD KEY `themes_theme_created_by_id_99c57b17_fk_core_user_id` (`created_by_id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `authors_author`
--
ALTER TABLE `authors_author`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=140;

--
-- AUTO_INCREMENT de la tabla `authors_nationality`
--
ALTER TABLE `authors_nationality`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=27;

--
-- AUTO_INCREMENT de la tabla `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=65;

--
-- AUTO_INCREMENT de la tabla `books_book`
--
ALTER TABLE `books_book`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=160;

--
-- AUTO_INCREMENT de la tabla `core_user`
--
ALTER TABLE `core_user`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `core_user_groups`
--
ALTER TABLE `core_user_groups`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `core_user_user_permissions`
--
ALTER TABLE `core_user_user_permissions`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=29;

--
-- AUTO_INCREMENT de la tabla `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=46;

--
-- AUTO_INCREMENT de la tabla `language_language`
--
ALTER TABLE `language_language`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT de la tabla `publishing_houses_publishinghouse`
--
ALTER TABLE `publishing_houses_publishinghouse`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=85;

--
-- AUTO_INCREMENT de la tabla `search_search`
--
ALTER TABLE `search_search`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `themes_theme`
--
ALTER TABLE `themes_theme`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `authors_author`
--
ALTER TABLE `authors_author`
  ADD CONSTRAINT `authors_author_created_by_id_9275319a_fk_core_user_id` FOREIGN KEY (`created_by_id`) REFERENCES `core_user` (`id`),
  ADD CONSTRAINT `authors_author_nationality_id_f5145aac_fk_authors_nationality_id` FOREIGN KEY (`nationality_id`) REFERENCES `authors_nationality` (`id`);

--
-- Filtros para la tabla `authors_nationality`
--
ALTER TABLE `authors_nationality`
  ADD CONSTRAINT `authors_nationality_created_by_id_a9ad8ef4_fk_core_user_id` FOREIGN KEY (`created_by_id`) REFERENCES `core_user` (`id`);

--
-- Filtros para la tabla `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Filtros para la tabla `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Filtros para la tabla `books_book`
--
ALTER TABLE `books_book`
  ADD CONSTRAINT `books_book_author_id_8b91747b_fk_authors_author_id` FOREIGN KEY (`author_id`) REFERENCES `authors_author` (`id`),
  ADD CONSTRAINT `books_book_language_id_b9f55b1a_fk_language_language_id` FOREIGN KEY (`language_id`) REFERENCES `language_language` (`id`),
  ADD CONSTRAINT `books_book_publishing_house_id_8e10b8c7_fk_publishin` FOREIGN KEY (`publishing_house_id`) REFERENCES `publishing_houses_publishinghouse` (`id`),
  ADD CONSTRAINT `books_book_theme_id_6b0b49c2_fk_themes_theme_id` FOREIGN KEY (`theme_id`) REFERENCES `themes_theme` (`id`);

--
-- Filtros para la tabla `core_user_groups`
--
ALTER TABLE `core_user_groups`
  ADD CONSTRAINT `core_user_groups_group_id_fe8c697f_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `core_user_groups_user_id_70b4d9b8_fk_core_user_id` FOREIGN KEY (`user_id`) REFERENCES `core_user` (`id`);

--
-- Filtros para la tabla `core_user_user_permissions`
--
ALTER TABLE `core_user_user_permissions`
  ADD CONSTRAINT `core_user_user_permi_permission_id_35ccf601_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `core_user_user_permissions_user_id_085123d3_fk_core_user_id` FOREIGN KEY (`user_id`) REFERENCES `core_user` (`id`);

--
-- Filtros para la tabla `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_core_user_id` FOREIGN KEY (`user_id`) REFERENCES `core_user` (`id`);

--
-- Filtros para la tabla `publishing_houses_publishinghouse`
--
ALTER TABLE `publishing_houses_publishinghouse`
  ADD CONSTRAINT `publishing_houses_pu_created_by_id_4da9abaf_fk_core_user` FOREIGN KEY (`created_by_id`) REFERENCES `core_user` (`id`);

--
-- Filtros para la tabla `themes_theme`
--
ALTER TABLE `themes_theme`
  ADD CONSTRAINT `themes_theme_created_by_id_99c57b17_fk_core_user_id` FOREIGN KEY (`created_by_id`) REFERENCES `core_user` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

