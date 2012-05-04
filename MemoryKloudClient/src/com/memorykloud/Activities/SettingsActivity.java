package com.memorykloud.Activities;

import com.memorykloud.R;

import android.app.Activity;
import android.app.ListActivity;
import android.os.Bundle;
import android.widget.*;
import android.widget.AdapterView.OnItemClickListener;
import android.view.View;

public class SettingsActivity extends Activity {
    /** Called when the activity is first created. */
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
		setContentView(R.layout.mk_profile);
    }
    public void editProfile_Click(View view){
    	setContentView(R.layout.mk_profile_edit);
    }    
    
}