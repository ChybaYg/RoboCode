package project;

import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

import robocode.Bullet;
import robocode.DeathEvent;
import robocode.RoundEndedEvent;
import robocode.ScannedRobotEvent;

public class Collector extends Robot { 
    private List<Observation> observations;
    private Observation observation;

    public Collector() {
        super();

        observations = new ArrayList<>();
        observation = null;
    }

    // here we can collect all information, when we scan some enemy tank
    @Override
    public void onScannedRobot(ScannedRobotEvent e) {
        super.onScannedRobot(e);

        observation = new Observation(getX(), getY(), e.getBearing(), getHeading(), getGunHeading(), e.getDistance(), e.getHeading(), e.getVelocity());
    }

    //adding the last observation after fireing the bullet
    @Override
    public void onFired(Bullet bullet) {
        if (bullet != null) {
            observations.add(observation);
            observation.setBullet(bullet);
        }
    }

    // this method saves data on the end of round
    @Override
    public void onRoundEnded(RoundEndedEvent e) {
        super.onRoundEnded(e);    //scanning enemy tank data - written in Observation class
        
        save();
    }

    // method for adding info to CSV file
    private void save() {
        // open observations file in append mode
        try (FileWriter writer = new FileWriter("observations.csv", true)) {
            for (Observation observation: observations) 
                writer.write(observation.toString());

            writer.close();
        } catch (IOException e) { e.printStackTrace(); }
    }
}
