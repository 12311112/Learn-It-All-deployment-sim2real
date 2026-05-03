## Deployment Pipeline

This document focuses on the final real-world deployment stage of the project. The core deployment workflow is shown below:

<p align="center">
  <img width="696" height="340" alt="Deployment Pipeline" src="https://github.com/user-attachments/assets/72d2be25-941a-4f7c-a7f3-33cf587c0bdb" />
</p>

The main goal of this stage is to deploy the control policy implemented and verified in MuJoCo onto the physical quadruped robot. In this project, MuJoCo serves as the key simulation environment for policy development, validation, and sim-to-real preparation before real-world deployment.

In addition to the reinforcement learning-based deployment pipeline, this project also provides an educational inverse kinematics controller for the robot. This IK controller is not the core deployment method of this project. Instead, it is included to help beginners understand the basic motion control principles of quadruped robots, including leg kinematics, gait generation, and low-level command execution. Through this part, users can learn how a quadruped robot can be controlled using a traditional model-based method before moving to learning-based control policies.

The IK controller part is inspired by the following open-source project:

https://github.com/runeharlyk/SpotMicroESP32-Leika

The referenced project provides a PyBullet-based simulation process. Its core workflow is shown below:

<p align="center">
  <img width="928" height="641" alt="PyBullet IK Simulation Workflow" src="https://github.com/user-attachments/assets/5cff40be-b050-48eb-afab-7eb8ee54949e" />
</p>

Since the author was traveling while preparing this documentation, access to the physical robot platform was temporarily unavailable. Therefore, the environment configuration for the onboard computing unit has not yet been fully verified on the real robot.

The setup instructions for the onboard computing unit and the complete real-robot deployment process will be added in future updates.

