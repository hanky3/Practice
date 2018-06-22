package com.lge.conn.testbleplayer;

import android.app.Service;
import android.content.Intent;
import android.media.MediaPlayer;
import android.os.IBinder;
import android.widget.Toast;

public class MyPlayerService extends Service {
    public MyPlayerService() {
    }

    MediaPlayer mediaPlayer;

    @Override
    public void onCreate() {
        super.onCreate();

        if (mediaPlayer != null) {
            mediaPlayer.stop();
            mediaPlayer.release();
        }
        mediaPlayer = MediaPlayer.create(this, R.raw.loop);
        mediaPlayer.setLooping(false);
    }

    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        Toast.makeText(this, "음악 Play!!", Toast.LENGTH_SHORT).show();
        // start music play
        //MediaPlayer mediaPlayer = MediaPlayer.create(this, )
        mediaPlayer.start();

        return super.onStartCommand(intent, flags, startId);
    }

    @Override
    public void onDestroy() {
        super.onDestroy();
        if (mediaPlayer != null) {
            mediaPlayer.stop();
            mediaPlayer.release();
            mediaPlayer = null;
        }
        // stop music play
        Toast.makeText(this, "음악 Stop!!", Toast.LENGTH_SHORT).show();
    }

    @Override
    public IBinder onBind(Intent intent) {
        // TODO: Return the communication channel to the service.
        throw new UnsupportedOperationException("Not yet implemented");
    }
}
