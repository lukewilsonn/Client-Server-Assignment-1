/*
  Warnings:

  - You are about to drop the `Tag` table. If the table is not empty, all the data it contains will be lost.
  - Added the required column `Tag` to the `Order` table without a default value. This is not possible if the table is not empty.

*/
-- DropForeignKey
ALTER TABLE `Tag` DROP FOREIGN KEY `Tag_orderId_fkey`;

-- AlterTable
ALTER TABLE `Order` ADD COLUMN `Tag` JSON NOT NULL;

-- DropTable
DROP TABLE `Tag`;
