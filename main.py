#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
喝水提醒程序 - 主入口
使用 MVC 架构重构
"""

import sys
from src.reminder import ReminderController, get_logger


def main():
    """主函数"""
    logger = get_logger()
    logger.info("喝水提醒程序启动")
    
    try:
        controller = ReminderController()
        controller.run()
    except KeyboardInterrupt:
        logger.info("程序被用户中断")
        sys.exit(0)
    except Exception as e:
        logger.error(f"程序发生错误: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
