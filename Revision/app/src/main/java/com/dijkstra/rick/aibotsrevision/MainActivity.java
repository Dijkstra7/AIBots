package com.dijkstra.rick.aibotsrevision;

import androidx.appcompat.app.AppCompatActivity;

import android.content.res.Resources;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonArrayRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONArray;
import org.json.JSONException;

public class MainActivity extends AppCompatActivity implements View.OnClickListener {

    private RequestQueue queue;
    private String server;
    private Resources res;

    private Button loadButton;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        res = getResources();
        queue = Volley.newRequestQueue(this);
        server = res.getString(R.string.server);
        mapGUI();
    }

    private void mapGUI() {
        loadButton = findViewById(R.id.loadButton);
        loadButton.setOnClickListener(this);
    }

    public void loadBestTribes(){
        String url = server + "/getBestTribes";
        JsonArrayRequest mReq = new JsonArrayRequest(
                Request.Method.GET,
                url,
                null,
                new Response.Listener<JSONArray>() {
                    @Override
                    public void onResponse(JSONArray response) {
                        try {
                            tryLoadTribes(response);
                        }
                        catch (JSONException exception){
                            loadButton.setText(res.getString(R.string.parsing_error));
                        }
                    }
                },
                new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        loadButton.setText(res.getString(R.string.loading_error));
                    }
                }
            );
        queue.add(mReq);
    }

    public void tryLoadTribes(JSONArray response_tribes) throws JSONException {
        int amount_tribes = response_tribes.length();
        Tribe[] tribes = new Tribe[amount_tribes];
        for (int i = 0; i < amount_tribes; i++) {
            tribes[i] = new Tribe(response_tribes.getJSONObject(i));
        }
        loadButton.setText(String.format("Loaded tribes starting with%s", tribes[0].getTribeName()));
    }

    @Override
    public void onClick(View v) {
        Log.d("mainView", "Button clicked");
        if (v == loadButton){
            loadBestTribes();
        }
    }
}
