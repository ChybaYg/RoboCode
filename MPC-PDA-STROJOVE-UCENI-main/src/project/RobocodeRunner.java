package project;

import robocode.control.BattleSpecification;
import robocode.control.BattlefieldSpecification;
import robocode.control.RobocodeEngine;
import robocode.control.RobotSpecification;

public class RobocodeRunner {

    // define the static size of game map
	public static int width = 800;
	public static int height = 600;

	private static String robots = "project.Collector*, sample.Walls";

	public static void main(String[] args) {
		System.setProperty("NOSECURITY", "true");

		RobocodeEngine engine = new RobocodeEngine();

		engine.addBattleListener(new BattleObserver());

		engine.setVisible(true);

		BattlefieldSpecification battlefield = new BattlefieldSpecification(width, height);

		RobotSpecification[] selectedRobots = engine.getLocalRepository(robots);

		BattleSpecification battleSpec = new BattleSpecification(500, battlefield, selectedRobots);

		engine.runBattle(battleSpec, true);

		engine.close();

		System.exit(0);
	}
}
