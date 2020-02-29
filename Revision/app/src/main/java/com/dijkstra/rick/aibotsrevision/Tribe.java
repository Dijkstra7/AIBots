package com.dijkstra.rick.aibotsrevision;

import android.os.Parcel;
import android.os.Parcelable;

import org.json.JSONObject;

public class Tribe implements Parcelable{

    public Tribe(JSONObject tribe){

    }

    protected Tribe(Parcel in) {
    }

    public static final Creator<Tribe> CREATOR = new Creator<Tribe>() {
        @Override
        public Tribe createFromParcel(Parcel in) {
            return new Tribe(in);
        }

        @Override
        public Tribe[] newArray(int size) {
            return new Tribe[size];
        }
    };

    @Override
    public int describeContents() {
        return 0;
    }

    @Override
    public void writeToParcel(Parcel dest, int flags) {
    }
}
