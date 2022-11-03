/**
 * Copyright (c) 2001-2017 Mathew A. Nelson and Robocode contributors
 * All rights reserved. This program and the accompanying materials
 * are made available under the terms of the Eclipse Public License v1.0
 * which accompanies this distribution, and is available at
 * http://robocode.sourceforge.net/license/epl-v10.html
 */
package sample;

import robocode.*;

import java.awt.*;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;
import java.util.ArrayList;

/**
 * Crazy - a sample robot by Mathew Nelson.
 * <p>
 * This robot moves around in a crazy pattern.
 *
 * @author Mathew A. Nelson (original)
 * @author Flemming N. Larsen (contributor)
 */
public class CrazyAI extends AdvancedRobot {
	boolean learningMode = false;

	private ArrayList<CrazyAI.State> states = new ArrayList<>();
	boolean movingForward;
	private Socket clientSocket;
	private PrintWriter out;
	private BufferedReader in;

	/**
	 * run: Crazy's main run function
	 */
	public void run() {
		try {
			connect("localhost", 5000);
		} catch (Exception e) {
			e.printStackTrace();
			System.exit(0);
		}
		// Let server know if this game is learning or AI
		if (learningMode) {
			this.out.write("0000");
			this.out.flush();
		} else {
			this.out.write("1111");
			this.out.flush();
		}

		// Set colors
		setBodyColor(new Color(0, 200, 0));
		setGunColor(new Color(0, 150, 50));
		setRadarColor(new Color(0, 100, 100));
		setBulletColor(new Color(255, 255, 100));
		setScanColor(new Color(255, 200, 200));

		// Loop forever
		while (true) {
			// Tell the game we will want to move ahead 40000 -- some large number
			setAhead(40000);
			movingForward = true;
			// Tell the game we will want to turn right 90
			setTurnRight(90);
			// At this point, we have indicated to the game that *when we do something*,
			// we will want to move ahead and turn right. That's what "set" means.
			// It is important to realize we have not done anything yet!
			// In order to actually move, we'll want to call a method that
			// takes real time, such as waitFor.
			// waitFor actually starts the action -- we start moving and turning.
			// It will not return until we have finished turning.
			waitFor(new TurnCompleteCondition(this));
			// Note: We are still moving ahead now, but the turn is complete.
			// Now we'll turn the other way...
			setTurnLeft(180);
			// ... and wait for the turn to finish ...
			waitFor(new TurnCompleteCondition(this));
			// ... then the other way ...
			setTurnRight(180);
			// .. and wait for that turn to finish.
			waitFor(new TurnCompleteCondition(this));
			// then back to the top to do it all again
		}
	}

	/**
	 * onHitWall: Handle collision with wall.
	 */
	public void onHitWall(HitWallEvent e) {
		// Bounce off!
		reverseDirection();
	}

	/**
	 * reverseDirection: Switch from ahead to back & vice versa
	 */
	public void reverseDirection() {
		if (movingForward) {
			setBack(40000);
			movingForward = false;
		} else {
			setAhead(40000);
			movingForward = true;
		}
	}

	/**
	 * onScannedRobot: Fire!
	 */
	public void onScannedRobot(ScannedRobotEvent e) {

		if (learningMode) {
			State newState = new CrazyAI.State(getX(), getY(), getHeading(), e.getDistance(), e.getHeading(),
					e.getVelocity());

			// fire
			Bullet bullet = fireBullet(1);

			newState.addBullet(bullet);
			this.states.add(newState);

		} else {
			// AI Mode
			State newState = new CrazyAI.State(getX(), getY(), getHeading(), e.getDistance(), e.getHeading(),
					e.getVelocity());
			log(newState.toString());

			// Should I shoot in this state?
			boolean aiResponse = false;

			try {
				aiResponse = requestAction(newState);
			} catch (IOException e1) {
				e1.printStackTrace();
			}

			if (aiResponse) {
				log("Shooting!");
				fire(1);
			} else {
				log("Not shooting!");
			}

		}

	}

	/**
	 * onHitRobot: Back up!
	 */
	public void onHitRobot(HitRobotEvent e) {
		// If we're moving the other robot, reverse!
		if (e.isMyFault()) {
			reverseDirection();
		}
	}

	public void connect(String hostname, int port) throws IOException {
		this.clientSocket = new Socket(hostname, port);
		this.out = new PrintWriter(clientSocket.getOutputStream());
		this.in = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));
	}

	public boolean requestAction(State state) throws IOException {
		boolean shouldShoot = false;

		this.out.write(state.toString());
		this.out.flush();

		String resp = in.readLine();

		if (resp.equals("shoot")) {
			shouldShoot = true;
		}

		return shouldShoot;
	}

	public void log(String log) {
		File logFile = new File("log.txt");
		try (FileWriter writer = new FileWriter(logFile, true)) {
			writer.write(log + "\n");
			writer.close();
		} catch (IOException e) {
			e.printStackTrace();
		}

	}

	@Override
	public void onRoundEnded(RoundEndedEvent e) {
		if (learningMode) {
			for (CrazyAI.State cur_state : this.states) {
				this.out.println(cur_state.toServerString());
				this.out.flush();
			}
		}
		try {
			clientSocket.close();
		} catch (IOException e1) {
			e1.printStackTrace();
		}
	}

	public class State {
		private double x;
		private double y;
		private double gunHeading;
		private double enemyDistance;
		private double enemyHeading;
		private double enemyVelocity;
		private Bullet bullet;

		public State(double x, double y, double gunHeading, double enemyDistance, double enemyHeading,
				double enemyVelocity) {
			this.x = x;
			this.y = y;
			this.gunHeading = gunHeading;
			this.enemyDistance = enemyDistance;
			this.enemyHeading = enemyHeading;
			this.enemyVelocity = enemyVelocity;
			this.bullet = null;

		}

		public void addBullet(Bullet bullet) {
			this.bullet = bullet;
		}

		public String toString() {
			return String.format("%.6f;%.6f;%.6f;%.6f;%.6f;%.6f", x, y, gunHeading, enemyDistance, enemyHeading,
					enemyVelocity);
		}

		public String toServerString() {
			int hit = 0;
			if (this.bullet != null) {
				if (this.bullet.getVictim() != null) {
					hit = 1;
				}
			}
			return String.format("%.6f;%.6f;%.6f;%.6f;%.6f;%.6f;%d", x, y, gunHeading, enemyDistance, enemyHeading,
					enemyVelocity, hit);

		}

	}
}
