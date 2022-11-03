package project;

import robocode.BattleResults;
import robocode.control.events.BattleAdaptor;
import robocode.control.events.BattleCompletedEvent;
import robocode.control.events.BattleErrorEvent;
import robocode.control.events.BattleFinishedEvent;
import robocode.control.events.BattleMessageEvent;
import robocode.control.events.BattleStartedEvent;

public class BattleObserver extends BattleAdaptor {

	//additional notation of game process

	public void onBattleStarted(BattleStartedEvent e) {
		System.out.println("-- Battle started --");
	}

	public void onBattleFinished(BattleFinishedEvent e) {
		if (e.isAborted())
			System.out.println("-- Battle aborted --");
		else
			System.out.println("-- Battle finished --");
	}

	public void onBattleCompleted(BattleCompletedEvent e) {
		System.out.println("-- Battle results --");

		for (BattleResults result : e.getSortedResults())
			System.out.println(result.getTeamLeaderName() + ": " + result.getScore());
	}

	public void onBattleMessage(BattleMessageEvent e) {
		System.out.println("Msg> " + e.getMessage());
	}

	public void onBattleError(BattleErrorEvent e) {
		System.out.println("Err> " + e.getError());
	}
}
