/*
 Navicat Premium Data Transfer

 Source Server         : SQL_lorry
 Source Server Type    : MySQL
 Source Server Version : 80200
 Source Host           : localhost:3306
 Source Schema         : mydormitory

 Target Server Type    : MySQL
 Target Server Version : 80200
 File Encoding         : 65001

 Date: 03/06/2024 12:59:21
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for dorm
-- ----------------------------
DROP TABLE IF EXISTS `dorm`;
CREATE TABLE `dorm`  (
  `Dormitory_id` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `Building_id` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `Dormitory_resident` int NULL DEFAULT NULL,
  `Electricity_balance` int NULL DEFAULT NULL,
  `stu_count` int NULL DEFAULT NULL,
  PRIMARY KEY (`Dormitory_id`) USING BTREE,
  INDEX `fk_building_number`(`Building_id` ASC) USING BTREE,
  CONSTRAINT `fk_building_number` FOREIGN KEY (`Building_id`) REFERENCES `dormitory_building` (`Building_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of dorm
-- ----------------------------
INSERT INTO `dorm` VALUES ('1001', '1C', 4, 0, 2);
INSERT INTO `dorm` VALUES ('1002', '1C', 4, 0, 0);
INSERT INTO `dorm` VALUES ('1003', '1C', 4, 0, 0);
INSERT INTO `dorm` VALUES ('1004', '1C', 4, 0, 0);
INSERT INTO `dorm` VALUES ('3002', '教工3', 4, 778, 3);
INSERT INTO `dorm` VALUES ('3011', '教工3', 4, 613, 2);
INSERT INTO `dorm` VALUES ('3091', '教工3', 4, 558, 0);
INSERT INTO `dorm` VALUES ('3092', '教工3', 4, 499, 0);
INSERT INTO `dorm` VALUES ('3103', '教工3', 4, 896, 0);
INSERT INTO `dorm` VALUES ('3110', '教工3', 4, 821, 0);
INSERT INTO `dorm` VALUES ('3117', '教工3', 4, 72, 0);
INSERT INTO `dorm` VALUES ('3122', '教工3', 4, 118, 0);
INSERT INTO `dorm` VALUES ('3130', '教工3', 4, 12, 0);
INSERT INTO `dorm` VALUES ('3133', '教工3', 4, 109, 0);
INSERT INTO `dorm` VALUES ('3149', '教工3', 4, 84, 0);
INSERT INTO `dorm` VALUES ('3157', '教工3', 4, 498, 0);
INSERT INTO `dorm` VALUES ('3160', '教工3', 4, 630, 0);
INSERT INTO `dorm` VALUES ('3166', '教工3', 4, 180, 0);
INSERT INTO `dorm` VALUES ('3171', '教工3', 4, 122, 0);
INSERT INTO `dorm` VALUES ('3172', '教工3', 4, 948, 0);
INSERT INTO `dorm` VALUES ('3177', '教工3', 4, 234, 0);
INSERT INTO `dorm` VALUES ('3181', '教工3', 4, 63, 0);
INSERT INTO `dorm` VALUES ('3208', '教工3', 4, 150, 0);
INSERT INTO `dorm` VALUES ('3218', '教工3', 4, 344, 0);
INSERT INTO `dorm` VALUES ('3221', '教工3', 4, 358, 0);
INSERT INTO `dorm` VALUES ('3240', '教工3', 4, 151, 0);
INSERT INTO `dorm` VALUES ('3241', '教工3', 4, 626, 0);
INSERT INTO `dorm` VALUES ('3242', '教工3', 4, 269, 0);
INSERT INTO `dorm` VALUES ('3243', '教工3', 4, 237, 0);
INSERT INTO `dorm` VALUES ('3255', '教工3', 4, 2, 0);
INSERT INTO `dorm` VALUES ('3259', '教工3', 4, 827, 0);
INSERT INTO `dorm` VALUES ('3290', '教工3', 4, 877, 0);
INSERT INTO `dorm` VALUES ('3306', '教工3', 4, 86, 0);
INSERT INTO `dorm` VALUES ('3308', '教工3', 4, 844, 0);
INSERT INTO `dorm` VALUES ('3310', '教工3', 4, 63, 0);
INSERT INTO `dorm` VALUES ('3314', '教工3', 4, 690, 0);
INSERT INTO `dorm` VALUES ('3318', '教工3', 4, 329, 0);
INSERT INTO `dorm` VALUES ('3319', '教工3', 4, 100, 1);
INSERT INTO `dorm` VALUES ('3320', '教工3', 4, 100, 3);
INSERT INTO `dorm` VALUES ('3338', '教工3', 4, 72, 0);
INSERT INTO `dorm` VALUES ('3341', '教工3', 4, 935, 0);
INSERT INTO `dorm` VALUES ('3347', '教工3', 4, 769, 0);
INSERT INTO `dorm` VALUES ('3349', '教工3', 4, 391, 0);
INSERT INTO `dorm` VALUES ('3350', '教工3', 4, 83, 0);
INSERT INTO `dorm` VALUES ('3352', '教工3', 4, 898, 0);
INSERT INTO `dorm` VALUES ('3353', '教工3', 4, 25, 0);
INSERT INTO `dorm` VALUES ('3354', '教工3', 4, 106, 0);
INSERT INTO `dorm` VALUES ('3358', '教工3', 4, 271, 0);
INSERT INTO `dorm` VALUES ('3362', '教工3', 4, 275, 0);
INSERT INTO `dorm` VALUES ('3364', '教工3', 4, 941, 0);
INSERT INTO `dorm` VALUES ('3368', '教工3', 4, 488, 0);
INSERT INTO `dorm` VALUES ('3371', '教工3', 4, 323, 0);
INSERT INTO `dorm` VALUES ('3392', '教工3', 4, 968, 0);
INSERT INTO `dorm` VALUES ('3406', '教工3', 4, 702, 0);
INSERT INTO `dorm` VALUES ('3414', '教工3', 4, 632, 0);
INSERT INTO `dorm` VALUES ('3418', '教工3', 4, 649, 0);
INSERT INTO `dorm` VALUES ('3422', '教工3', 4, 720, 0);
INSERT INTO `dorm` VALUES ('3425', '教工3', 4, 68, 0);
INSERT INTO `dorm` VALUES ('3428', '教工3', 4, 453, 0);
INSERT INTO `dorm` VALUES ('3432', '教工3', 4, 455, 0);
INSERT INTO `dorm` VALUES ('3438', '教工3', 4, 776, 0);
INSERT INTO `dorm` VALUES ('3442', '教工3', 4, 136, 0);
INSERT INTO `dorm` VALUES ('3448', '教工3', 4, 532, 0);
INSERT INTO `dorm` VALUES ('3450', '教工3', 4, 0, 0);
INSERT INTO `dorm` VALUES ('3468', '教工3', 4, 276, 0);
INSERT INTO `dorm` VALUES ('3471', '教工3', 4, 211, 0);
INSERT INTO `dorm` VALUES ('3488', '教工3', 4, 618, 0);
INSERT INTO `dorm` VALUES ('3490', '教工3', 4, 593, 0);
INSERT INTO `dorm` VALUES ('3492', '教工3', 4, 484, 0);
INSERT INTO `dorm` VALUES ('3494', '教工3', 4, 341, 0);
INSERT INTO `dorm` VALUES ('3504', '教工3', 4, 51, 0);
INSERT INTO `dorm` VALUES ('3505', '教工3', 4, 469, 0);
INSERT INTO `dorm` VALUES ('3517', '教工3', 4, 848, 0);
INSERT INTO `dorm` VALUES ('3521', '教工3', 4, 709, 0);
INSERT INTO `dorm` VALUES ('3530', '教工3', 4, 97, 0);
INSERT INTO `dorm` VALUES ('3532', '教工3', 4, 651, 0);
INSERT INTO `dorm` VALUES ('3551', '教工3', 4, 485, 0);
INSERT INTO `dorm` VALUES ('3557', '教工3', 4, 937, 0);
INSERT INTO `dorm` VALUES ('3564', '教工3', 4, 285, 0);
INSERT INTO `dorm` VALUES ('3570', '教工3', 4, 533, 0);
INSERT INTO `dorm` VALUES ('3571', '教工3', 4, 764, 0);
INSERT INTO `dorm` VALUES ('3575', '教工3', 4, 116, 0);
INSERT INTO `dorm` VALUES ('3578', '教工3', 4, 844, 0);
INSERT INTO `dorm` VALUES ('3579', '教工3', 4, 596, 0);
INSERT INTO `dorm` VALUES ('3582', '教工3', 4, 816, 0);
INSERT INTO `dorm` VALUES ('3583', '教工3', 4, 479, 0);
INSERT INTO `dorm` VALUES ('3584', '教工3', 4, 523, 0);
INSERT INTO `dorm` VALUES ('3594', '教工3', 4, 363, 0);
INSERT INTO `dorm` VALUES ('3606', '教工3', 4, 107, 0);
INSERT INTO `dorm` VALUES ('3607', '教工3', 4, 925, 0);
INSERT INTO `dorm` VALUES ('3611', '教工3', 4, 872, 0);
INSERT INTO `dorm` VALUES ('3617', '教工3', 4, 921, 0);
INSERT INTO `dorm` VALUES ('3622', '教工3', 4, 466, 0);
INSERT INTO `dorm` VALUES ('3628', '教工3', 4, 490, 0);
INSERT INTO `dorm` VALUES ('3632', '教工3', 4, 249, 0);
INSERT INTO `dorm` VALUES ('3636', '教工3', 4, 501, 0);
INSERT INTO `dorm` VALUES ('3639', '教工3', 4, 47, 0);
INSERT INTO `dorm` VALUES ('5002', '5D', 4, 100, 0);
INSERT INTO `dorm` VALUES ('5417', '5D', 4, 100, 0);

-- ----------------------------
-- Table structure for dorm_maintain
-- ----------------------------
DROP TABLE IF EXISTS `dorm_maintain`;
CREATE TABLE `dorm_maintain`  (
  `job_number` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `Job_Content` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`job_number`) USING BTREE,
  CONSTRAINT `fk_dorm_mantain_job_number` FOREIGN KEY (`job_number`) REFERENCES `dormitorystaff` (`job_number`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of dorm_maintain
-- ----------------------------
INSERT INTO `dorm_maintain` VALUES ('20242311', NULL);
INSERT INTO `dorm_maintain` VALUES ('20242312', '5B宿舍楼维修人员');
INSERT INTO `dorm_maintain` VALUES ('20242315', NULL);
INSERT INTO `dorm_maintain` VALUES ('20242316', NULL);
INSERT INTO `dorm_maintain` VALUES ('20242317', '教3宿舍楼维修员');

-- ----------------------------
-- Table structure for dorm_supervisor
-- ----------------------------
DROP TABLE IF EXISTS `dorm_supervisor`;
CREATE TABLE `dorm_supervisor`  (
  `job_number` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `Job_Content` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`job_number`) USING BTREE,
  CONSTRAINT `fk_dorm_supervisor_job_number` FOREIGN KEY (`job_number`) REFERENCES `dormitorystaff` (`job_number`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of dorm_supervisor
-- ----------------------------
INSERT INTO `dorm_supervisor` VALUES ('20241311', NULL);
INSERT INTO `dorm_supervisor` VALUES ('20241312', NULL);
INSERT INTO `dorm_supervisor` VALUES ('20241313', NULL);
INSERT INTO `dorm_supervisor` VALUES ('20241314', NULL);
INSERT INTO `dorm_supervisor` VALUES ('20241315', '宿舍二级管理员');
INSERT INTO `dorm_supervisor` VALUES ('20241316', NULL);
INSERT INTO `dorm_supervisor` VALUES ('88888888', '一级管理员');

-- ----------------------------
-- Table structure for dormitory_building
-- ----------------------------
DROP TABLE IF EXISTS `dormitory_building`;
CREATE TABLE `dormitory_building`  (
  `Building_id` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `Building_location` varchar(40) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `manager_id` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `dorm_count` int NULL DEFAULT NULL,
  `sex` char(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `maintain_id` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`Building_id`) USING BTREE,
  INDEX `fk_manager_id`(`manager_id` ASC) USING BTREE,
  CONSTRAINT `fk_manager_id` FOREIGN KEY (`manager_id`) REFERENCES `dorm_supervisor` (`job_number`) ON DELETE SET NULL ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of dormitory_building
-- ----------------------------
INSERT INTO `dormitory_building` VALUES ('1C', '文科组团', '20241311', 4, '男', '20242311');
INSERT INTO `dormitory_building` VALUES ('5B', '理科组团', '20241312', 0, '女', '20242312');
INSERT INTO `dormitory_building` VALUES ('5C', '理科组团', '20241314', 0, '女', '20242315');
INSERT INTO `dormitory_building` VALUES ('5D', '理科组团', '20241313', 2, '男', '20242316');
INSERT INTO `dormitory_building` VALUES ('教工3', '理科组团', '20241315', 93, '男', '20242317');

-- ----------------------------
-- Table structure for dormitorystaff
-- ----------------------------
DROP TABLE IF EXISTS `dormitorystaff`;
CREATE TABLE `dormitorystaff`  (
  `job_number` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `Sta_age` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `Sta_Sex` char(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `Sta_name` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '123456',
  `phone` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`job_number`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of dormitorystaff
-- ----------------------------
INSERT INTO `dormitorystaff` VALUES ('20241311', '26', 'm', '徐致远', 'zx6', '15865651234');
INSERT INTO `dormitorystaff` VALUES ('20241312', '28', 'w', '徐子韬', 'zitxu2014', '15866359875');
INSERT INTO `dormitorystaff` VALUES ('20241313', '24', 'm', '董云熙', 'yunxi125', '19566889534');
INSERT INTO `dormitorystaff` VALUES ('20241314', '23', 'w', '李杰宏', 'lij', '19589634856');
INSERT INTO `dormitorystaff` VALUES ('20241315', '36', 'm', '金秀英', 'jin5', '19899886598');
INSERT INTO `dormitorystaff` VALUES ('20241316', '41', 'm', '刘宏旺', '123456', '15668936548');
INSERT INTO `dormitorystaff` VALUES ('20242311', '23', 'm', '李一名', '123456', '15668924548');
INSERT INTO `dormitorystaff` VALUES ('20242312', '24', 'm', '张宏伟', '123456', '15665786548');
INSERT INTO `dormitorystaff` VALUES ('20242315', '25', 'm', '王潇阳', '123456', '15142936548');
INSERT INTO `dormitorystaff` VALUES ('20242316', '26', 'm', '驰岚', '123456', '15668967898');
INSERT INTO `dormitorystaff` VALUES ('20242317', '27', 'm', '季淮文', '123456', '15614936548');
INSERT INTO `dormitorystaff` VALUES ('88888888', '35', 'w', '超级管理员', '1234567', '16866886858');

-- ----------------------------
-- Table structure for evaluate
-- ----------------------------
DROP TABLE IF EXISTS `evaluate`;
CREATE TABLE `evaluate`  (
  `Student_id` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `apply_timestamp` timestamp NOT NULL,
  `evaluate_timestamp` timestamp NOT NULL,
  `apply_description` varchar(40) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `evaluate_description` varchar(40) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`Student_id`, `apply_timestamp`, `evaluate_timestamp`) USING BTREE,
  INDEX `fk_evaluate_apply_timestamp`(`apply_timestamp` ASC) USING BTREE,
  INDEX `fk_evaluate_apply_description`(`apply_description` ASC) USING BTREE,
  CONSTRAINT `fk_evaluate_apply_description` FOREIGN KEY (`apply_description`) REFERENCES `fix` (`detail`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `fk_evaluate_apply_timestamp` FOREIGN KEY (`apply_timestamp`) REFERENCES `fix` (`timestamp`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `fk_evaluate_student_id` FOREIGN KEY (`Student_id`) REFERENCES `student` (`Student_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of evaluate
-- ----------------------------
INSERT INTO `evaluate` VALUES ('2510003', '2024-06-02 16:51:08', '2024-06-03 12:10:12', '3320阳台门损坏', '好，善');
INSERT INTO `evaluate` VALUES ('2510011', '2024-06-02 16:00:32', '2024-06-02 16:27:58', '1\n', '快一点');

-- ----------------------------
-- Table structure for fix
-- ----------------------------
DROP TABLE IF EXISTS `fix`;
CREATE TABLE `fix`  (
  `apply_student_id` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `detail` varchar(40) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `is_approved` tinyint(1) NULL DEFAULT 0,
  `is_fixed` tinyint(1) NULL DEFAULT 0,
  PRIMARY KEY (`apply_student_id`, `timestamp`) USING BTREE,
  INDEX `idx_fix_timestamp`(`timestamp` ASC) USING BTREE,
  INDEX `idx_fix_detail`(`detail` ASC) USING BTREE,
  CONSTRAINT `fk_fix_apply_student_id` FOREIGN KEY (`apply_student_id`) REFERENCES `student` (`Student_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of fix
-- ----------------------------
INSERT INTO `fix` VALUES ('2510003', '2024-06-02 16:51:06', '3320阳台门损坏', 1, 1);
INSERT INTO `fix` VALUES ('2510003', '2024-06-02 16:51:07', '3320阳台门损坏', 1, 1);
INSERT INTO `fix` VALUES ('2510003', '2024-06-02 16:51:08', '3320阳台门损坏', 1, 1);
INSERT INTO `fix` VALUES ('2510011', '2024-05-28 01:02:32', '1001宿舍灯具损坏\n', 0, 0);
INSERT INTO `fix` VALUES ('2510011', '2024-05-28 01:02:33', '1001宿舍灯具损坏\n', 0, 0);
INSERT INTO `fix` VALUES ('2510011', '2024-05-28 01:50:01', '1001宿舍灯具损坏\n', 0, 0);
INSERT INTO `fix` VALUES ('2510011', '2024-05-30 10:36:53', '1001宿舍空调损坏\n', 0, 0);
INSERT INTO `fix` VALUES ('2510011', '2024-05-30 10:37:00', '1001宿舍空调损坏\n', 0, 0);
INSERT INTO `fix` VALUES ('2510011', '2024-05-30 10:37:08', '1001宿舍空调损坏\n', 0, 0);
INSERT INTO `fix` VALUES ('2510011', '2024-06-02 16:00:29', '1\n', 0, 0);
INSERT INTO `fix` VALUES ('2510011', '2024-06-02 16:00:31', '1\n', 0, 0);
INSERT INTO `fix` VALUES ('2510011', '2024-06-02 16:00:32', '1\n', 0, 0);

-- ----------------------------
-- Table structure for student
-- ----------------------------
DROP TABLE IF EXISTS `student`;
CREATE TABLE `student`  (
  `Student_id` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `Dormitory_id` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `Stu_Name` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `Stu_Sex` char(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `Stu_seat` int NULL DEFAULT NULL,
  `Stu_College` varchar(25) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `login_password` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`Student_id`) USING BTREE,
  UNIQUE INDEX `CHK_seat`(`Dormitory_id` ASC, `Stu_seat` ASC) USING BTREE,
  CONSTRAINT `student_ibfk_1` FOREIGN KEY (`Dormitory_id`) REFERENCES `dorm` (`Dormitory_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of student
-- ----------------------------
INSERT INTO `student` VALUES ('2500461', '1002', '黎秀英', '男', 1, '电子信息与光学工程学院', 'xiuyingli');
INSERT INTO `student` VALUES ('2500701', '1002', '许安琪', '男', 2, '电子信息与光学工程学院', 'anxu');
INSERT INTO `student` VALUES ('2500788', '3011', '朱岚', '男', 2, '电子信息与光学工程学院', 'zhul');
INSERT INTO `student` VALUES ('2501123', '1002', '钱嘉伦', '男', 3, '电子信息与光学工程学院', '123456');
INSERT INTO `student` VALUES ('2501168', '3011', '傅子韬', '男', 4, '电子信息与光学工程学院', '123456');
INSERT INTO `student` VALUES ('2501567', '1002', '阎岚', '男', 4, '电子信息与光学工程学院', 'layan');
INSERT INTO `student` VALUES ('2501578', '3002', '任宇宁', '男', 2, '电子信息与光学工程学院', '123456');
INSERT INTO `student` VALUES ('2501710', '3002', '雷晓明', '男', 4, '电子信息与光学工程学院', 'leixiaoming');
INSERT INTO `student` VALUES ('2502085', NULL, '侯岚', '男', NULL, '电子信息与光学工程学院', 'houla');
INSERT INTO `student` VALUES ('2502153', NULL, '韦宇宁', '男', NULL, '电子信息与光学工程学院', 'wey83');
INSERT INTO `student` VALUES ('2502562', NULL, '郝睿', '男', NULL, '电子信息与光学工程学院', 'rui228');
INSERT INTO `student` VALUES ('2502929', '3002', '范宇宁', '男', 3, '电子信息与光学工程学院', 'fyuni');
INSERT INTO `student` VALUES ('2510003', '3320', '叶杰宏', '男', 2, '网络空间安全学院', 'jye109');
INSERT INTO `student` VALUES ('2510004', '3320', '苏睿', '男', 4, '网络空间安全学院', 'sur4');
INSERT INTO `student` VALUES ('2510005', NULL, '林子异', '男', NULL, '网络空间安全学院', 'zilin68');
INSERT INTO `student` VALUES ('2510007', '3320', '孟子韬', '男', 3, '网络空间安全学院', 'zme');
INSERT INTO `student` VALUES ('2510008', NULL, '李红', '男', NULL, 'None', '1234');
INSERT INTO `student` VALUES ('2510009', NULL, '李华', '男', NULL, '历史学院', '123456');
INSERT INTO `student` VALUES ('2510011', '1001', '刘旺旺', '男', 1, '计网', '123456');
INSERT INTO `student` VALUES ('2510012', NULL, '藤麗欣', '男', NULL, '电光', '123456');
INSERT INTO `student` VALUES ('2510058', NULL, '元家玲', '男', NULL, '电光', 'ykl49');
INSERT INTO `student` VALUES ('2510089', NULL, '樊國權', '男', NULL, '电光', 'kkf');
INSERT INTO `student` VALUES ('2510099', NULL, '冯嘉伦', '男', NULL, '电光', 'fejialun');
INSERT INTO `student` VALUES ('2552522', '3319', '高坤', '男', 3, '魔法学院', '123456');
INSERT INTO `student` VALUES ('2552523', NULL, '陈思', '男', NULL, '化学学院', NULL);
INSERT INTO `student` VALUES ('2555555', '1001', 'loose', '男', 2, 'None', '123456');

-- ----------------------------
-- View structure for student_info_with_dorm
-- ----------------------------
DROP VIEW IF EXISTS `student_info_with_dorm`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `student_info_with_dorm` AS select `s`.`Student_id` AS `Student_id`,`s`.`Stu_seat` AS `Stu_seat`,`s`.`Stu_College` AS `Stu_College`,`d`.`Dormitory_id` AS `Dormitory_id`,`d`.`Building_id` AS `Building_id`,`d`.`Electricity_balance` AS `Electricity_balance`,`b`.`Building_location` AS `Building_location`,`b`.`manager_id` AS `manager_id` from ((`student` `s` join `dorm` `d` on((`s`.`Dormitory_id` = `d`.`Dormitory_id`))) join `dormitory_building` `b` on((`d`.`Building_id` = `b`.`Building_id`)));

-- ----------------------------
-- Procedure structure for change_dorm_proc
-- ----------------------------
DROP PROCEDURE IF EXISTS `change_dorm_proc`;
delimiter ;;
CREATE PROCEDURE `change_dorm_proc`(IN new_dorm_id VARCHAR(20),
    IN new_seat INT,
    IN stu_id VARCHAR(20),
    OUT success BOOLEAN)
BEGIN
    #原宿舍号
    DECLARE old_dorm_id INT;
		#原、新宿舍人数
    DECLARE old_dorm_count INT;
    DECLARE new_dorm_count INT;
		#新宿舍容量
		DECLARE new_dorm_cap INT;
		#学生性别
    DECLARE stu_gender CHAR(2);
		#新宿舍性别
		DECLARE dorm_gender CHAR(2);
		#用于检查宿舍号是否存在和判断床位是否冲突的变量
		DECLARE dorm_count INT;
		DeCLARE is_seat_conflict INT;

    -- 获取原宿舍信息
    SELECT dormitory_id INTO old_dorm_id
    FROM student
    WHERE student_id = stu_id;

    -- 获取原宿舍的当前人数
    SELECT stu_count INTO old_dorm_count
    FROM dorm
    WHERE dormitory_id = old_dorm_id;

    -- 获取新宿舍的当前人数和性别
    SELECT stu_count, sex,Dormitory_resident 
		INTO new_dorm_count, dorm_gender,new_dorm_cap
    FROM dorm natural join dormitory_building
    WHERE dormitory_id = new_dorm_id;

    -- 开始事务
    START TRANSACTION;

    -- 1.检查宿舍号输入是否存在
    SELECT COUNT(*) INTO dorm_count FROM dorm WHERE dormitory_id = new_dorm_id;
    IF dorm_count = 0 THEN
        SET success = FALSE;
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = '输入的宿舍不存在！';
    END IF;

    -- 2.检查新旧宿舍是否相同
    IF old_dorm_id = new_dorm_id THEN
        SET success = FALSE;
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = '新旧宿舍不能相同！';
        ROLLBACK;
    END IF;
		
    -- 3.检查新宿舍stu_count属性是否等于dormitory_count属性
    IF new_dorm_cap = (SELECT stu_count FROM dorm WHERE dormitory_id = new_dorm_id) THEN
        SET success = FALSE;
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = '新宿舍容量已满！';
    END IF;
		
    -- 4.检查新宿舍是否与学生性别匹配
    IF dorm_gender != (SELECT stu_sex FROM student WHERE student_id = stu_id) THEN
        SET success = FALSE;
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = '请安排到性别一致的宿舍！';
        ROLLBACK;
    END IF;
		
    -- 5.检查床位号是否在新宿舍的容量范围内
    IF new_seat < 1 OR new_seat > new_dorm_cap THEN
        SET success = FALSE;
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = '新床位不合法！';
        ROLLBACK;
    END IF;

    -- 6.检查提交的床位号是否与原有床位号冲突
    SELECT COUNT(*) INTO is_seat_conflict 
    FROM student 
    WHERE dormitory_id = new_dorm_id AND stu_seat = new_seat;
    
    IF is_seat_conflict > 0 THEN
        SET success = FALSE;
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = '输入床位与已安排床位冲突！';
        ROLLBACK;
    END IF;

    -- 更新原宿舍的人数
    UPDATE dorm
    SET stu_count = old_dorm_count - 1
    WHERE dormitory_id = old_dorm_id;

    -- 更新学生的宿舍信息
    UPDATE student
    SET dormitory_id = new_dorm_id, stu_seat = new_seat
    WHERE student_id = stu_id;

    -- 更新新宿舍的人数
    UPDATE dorm
    SET stu_count = new_dorm_count + 1
    WHERE dormitory_id = new_dorm_id;

    SET success = TRUE;

    -- 提交事务
    COMMIT;
END
;;
delimiter ;

-- ----------------------------
-- Procedure structure for delete_dorm_procedure
-- ----------------------------
DROP PROCEDURE IF EXISTS `delete_dorm_procedure`;
delimiter ;;
CREATE PROCEDURE `delete_dorm_procedure`(IN dorm_id VARCHAR(20))
BEGIN
    DECLARE v_building_id VARCHAR(20);
    DECLARE v_dorm_count INT;

    -- 获取被删除宿舍所在的宿舍楼ID及其宿舍数量
    SELECT building_id, dorm_count INTO v_building_id, v_dorm_count FROM dormitory_building WHERE building_id = (SELECT building_id FROM dorm WHERE dormitory_id = dorm_id);

    -- 开始事务
    START TRANSACTION;

    -- 更新宿舍所在宿舍楼的宿舍数量减1
    UPDATE dormitory_building SET dorm_count = v_dorm_count - 1 WHERE building_id = v_building_id;

    -- 更新宿舍所有学生的宿舍号与床位置为空
    UPDATE student SET dormitory_id = NULL, stu_seat = NULL WHERE dormitory_id = dorm_id;

    -- 删除宿舍
    DELETE FROM dorm WHERE dormitory_id = dorm_id;

    -- 提交事务
    COMMIT;
END
;;
delimiter ;

-- ----------------------------
-- Triggers structure for table fix
-- ----------------------------
DROP TRIGGER IF EXISTS `check_fix_limit`;
delimiter ;;
CREATE TRIGGER `check_fix_limit` BEFORE INSERT ON `fix` FOR EACH ROW BEGIN
    DECLARE record_count INT;

    -- 获取当前学生在过去24小时内提交的记录数量
    SELECT COUNT(*) INTO record_count
    FROM fix
    WHERE apply_student_id = NEW.apply_student_id
    AND timestamp >= DATE_SUB(NOW(), INTERVAL 24 HOUR);

    -- 如果记录数量大于等于3，则抛出错误
    IF record_count >= 3 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = '您在过去24小时提交记录数量超过频率限制，请先耐心等待近期提交的报修结果！';
    END IF;
END
;;
delimiter ;

SET FOREIGN_KEY_CHECKS = 1;
