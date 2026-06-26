import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import sys
import tty
import termios

class TeleopNode(Node):
    def __init__(self):
        super().__init__('teleop_node')
        self.publisher = self.create_publisher(Twist, '/cmd_vel', 10)
        self.get_logger().info('Teleop Node Started')

    def get_key(self):
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)

        try:
            tty.setraw(fd)
            key = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)
        return key

    def run(self):
        while True:
            key = self.get_key()
            msg = Twist()

            if key == 'w':
                msg.linear.x = 0.5
            elif key == 's':
                msg.linear.x = -0.5
            elif key == 'a':
                msg.angular.z = 0.5
            elif key == 'd':
                msg.angular.z = -0.5
            elif key == 'q':
                self.get_logger().info('Quitting')
                break
            self.publisher.publish(msg)

def main(args = None):
    rclpy.init(args=args)
    node = TeleopNode()
    node.run()
    rclpy.shutdown()

if __name__ == '__main__':
    main()