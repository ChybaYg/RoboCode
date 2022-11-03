package project;

import java.util.Locale;

import robocode.Bullet;

class Observation {
    private double x;
    private double y;
    private double distance;
    private double enemyHeading;
    private double enemyDx;
    private double enemyDy;
    private double angle;
    private double gunToTurn;
    private double remainingToWall;
    private Bullet bullet;
    
    Observation(double x, double y, double bearing, double heading, double gunHeading, double distance, double enemyHeading, double enemyVelocity) {
        this.x = x;
        this.y = y;
        this.distance = distance;
        this.enemyHeading = enemyHeading % 90;

        // use velocity and enemyHeading to count the speed vector [Dx, Dy]
        this.enemyDx = enemyVelocity * Math.sin(Math.PI * enemyHeading / 180);
        this.enemyDy = enemyVelocity * Math.cos(Math.PI * enemyHeading / 180);

        // count enemy coordinates for remainingToWall parameter
        double enemyX = x + distance * Math.sin(Math.PI * (bearing + heading) / 180);
        double enemyY = y + distance * Math.cos(Math.PI * (bearing + heading) / 180);

        // how far from the wall the enemy robot is
        if (Math.abs(enemyDx) > 0.001)
            remainingToWall = (enemyDx > 0 ? RobocodeRunner.width - enemyX : enemyX) / RobocodeRunner.width;
        else if (Math.abs(enemyDy) > 0.001)
            remainingToWall = (enemyDy > 0 ? RobocodeRunner.height - enemyY : enemyY) / RobocodeRunner.height;
        else
            remainingToWall = 0;

        double relativeBulletHeading = toRelative(gunHeading - heading);
        // at what angle the gun must be turned to be pointed straight at the enemy
        this.gunToTurn = toRelative(bearing - relativeBulletHeading);

        // at what angle the enemy is turned relatively to gunHeading
        this.angle = Math.abs(toRelative(gunHeading - enemyHeading));

        normalize();
    }

    public void setBullet(Bullet bullet) {
        this.bullet = bullet;
    }

    @Override
    public String toString() {
        // don't use this observation if the bullet is still active·
        if (bullet.isActive())
            return "";
        
        return String.format(Locale.US, "%.6f;%.6f;%.6f;%.6f;%.6f;%.6f;%.6f;%d\n", gunToTurn, distance, angle, remainingToWall, enemyDx, enemyDy, enemyHeading, (bullet.getVictim() == null) ? 0 : 1);
    }

    private double toRelative(double input) {
    	return (input >= 180 ) ? -(360 - input) : (input < -180) ? (360 + input) : input;
    }

    // used for normalizing data to values from -1 to 1
    private void normalize() {
        this.x = (this.x - RobocodeRunner.width / 2) / RobocodeRunner.width;
        this.y = (this.y - RobocodeRunner.height / 2) / RobocodeRunner.height;
        this.distance /= Math.sqrt(RobocodeRunner.width * RobocodeRunner.width + RobocodeRunner.height * RobocodeRunner.height);
        this.enemyHeading /= 90;
        this.enemyDx /= 8;
        this.enemyDy /= 8;
        this.gunToTurn /= 180;
        this.angle /= 180;
    }
}
