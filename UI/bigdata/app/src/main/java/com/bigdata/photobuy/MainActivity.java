package com.bigdata.photobuy;

import android.app.ProgressDialog;
import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.net.Uri;
import android.os.AsyncTask;
import android.os.Bundle;
import android.os.Environment;
import android.os.StrictMode;
import android.provider.MediaStore;
import android.support.design.widget.FloatingActionButton;
import android.support.design.widget.Snackbar;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.util.Base64;
import android.util.Log;
import android.view.View;
import android.view.Menu;
import android.view.MenuItem;
import android.widget.AdapterView;
import android.widget.ImageButton;
import android.widget.ImageView;
import android.widget.Toast;

import com.loopj.android.http.AsyncHttpClient;
import com.loopj.android.http.AsyncHttpResponseHandler;
import com.loopj.android.http.JsonHttpResponseHandler;
import com.loopj.android.http.RequestParams;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedInputStream;
import java.io.BufferedReader;
import java.io.ByteArrayOutputStream;
import java.io.DataOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.UnsupportedEncodingException;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.ProtocolException;
import java.net.URI;
import java.net.URISyntaxException;
import java.net.URL;
import java.net.URLEncoder;
import java.nio.ByteBuffer;
import java.security.AccessControlContext;
import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.HashMap;
import java.util.Scanner;

import cz.msebera.android.httpclient.Header;
import cz.msebera.android.httpclient.NameValuePair;
import cz.msebera.android.httpclient.protocol.BasicHttpContext;
import cz.msebera.android.httpclient.protocol.HttpContext;

import static java.security.AccessController.getContext;

public class MainActivity extends AppCompatActivity {

    private static String root = null;
    private static String imageFolderPath = null;
    private String imageName = null;
    private static Uri fileUri = null;
    private static final int CAMERA_IMAGE_REQUEST=1;
    ImageView imageView = null;
    ImageButton send = null;
    Bundle extras = null;
    Bitmap imageBitmap = null;
    String image = null;


    ProgressDialog prgDialog;
    String encodedString;
    RequestParams params = new RequestParams();
    String imgPath, fileName;
    Bitmap bitmap, lesimg;
    private static int RESULT_LOAD_IMG = 1;
    private static int REQUEST_IMAGE_CAPTURE = 1;
    private static String TIME_STAMP="null";




    @Override
    protected void onCreate(Bundle savedInstanceState) {
        //StrictMode.VmPolicy.Builder builder = new StrictMode.VmPolicy.Builder();
        //StrictMode.setVmPolicy(builder.build());

        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        prgDialog = new ProgressDialog(this);
        prgDialog.setCancelable(false);

        Toolbar toolbar = (Toolbar) findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);
        imageView = (ImageView) findViewById(R.id.imageView);
        send = (ImageButton) findViewById(R.id.sendButton);
        //FloatingActionButton fab = (FloatingActionButton) findViewById(R.id.fab);
        root = Environment.getExternalStorageDirectory().toString()+"/PhotoBuy";
        imageFolderPath = root + "/saved_imageds";
        File imagesFolder = new File(imageFolderPath);
        imagesFolder.mkdirs();
        imageName = "test.png";
        File image = new File(imageFolderPath, imageName);
        fileUri = Uri.fromFile(image);
        imageView.setTag(imageFolderPath + File.separator + imageName);
        /*fab.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Snackbar.make(view, "Replace with your own action", Snackbar.LENGTH_LONG)
                        .setAction("Action", null).show();
            }
        });*/
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_main, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        //noinspection SimplifiableIfStatement
        if (id == R.id.action_settings) {
            return true;
        }

        return super.onOptionsItemSelected(item);
    }


    public void captureImage(View view){

        Intent takePictureIntent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);
        //takePictureIntent.putExtra(MediaStore.EXTRA_OUTPUT, fileUri);
        imageName="fname_" + String.valueOf(System.currentTimeMillis()) + ".jpg";
        fileUri = Uri.fromFile(new File(Environment.getExternalStorageDirectory(),"fname_" + String.valueOf(System.currentTimeMillis()) + ".jpg"));

        imageFolderPath = Environment.getExternalStorageDirectory()
                .toString() + "/Xiong_PIC/";
        imageName = new SimpleDateFormat("yyyyMMddHHmmss")
                .format(new Date()) + ".jpg";// 照片以格式化日期方式命名


        //takePictureIntent.putExtra(MediaStore.EXTRA_OUTPUT, fileUri);
        startActivityForResult(takePictureIntent, REQUEST_IMAGE_CAPTURE);


    }


    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        if(requestCode == CAMERA_IMAGE_REQUEST && resultCode == RESULT_OK){
            File imageFile = new File(imageFolderPath);

            extras = data.getExtras();
            imageBitmap = (Bitmap) extras.get("data");

            imageView.setImageBitmap(imageBitmap);
            imageView.setVisibility(View.VISIBLE);
            send.setVisibility(View.VISIBLE);

            params.put("filename", fileName);
        }
    }


    public void sendImage(View view) throws IOException {
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        String filename = "image.jpeg";
        imageBitmap = Bitmap.createScaledBitmap(imageBitmap,224, 224, false);

        /*byte[] imageBytes = baos.toByteArray();
        //Log.d("byte", new String(imageBytes));
        image = Base64.encodeToString(imageBytes, Base64.NO_WRAP);*/


        ByteBuffer byteBuffer = ByteBuffer.allocate(imageBitmap.getByteCount());
        imageBitmap.copyPixelsToBuffer(byteBuffer);
        byte[] imageBytes = byteBuffer.array();
        image = Base64.encodeToString(imageBytes, Base64.NO_WRAP);

        Log.d("length",String.valueOf(image.length()));

        getResponse(image);
    }


    public void getResponse(String image){
        String searchStr="http://52.202.23.209:10038/query";
        AsyncHttpClient client = new AsyncHttpClient();
        RequestParams params = new RequestParams();
        params.put("data", image);
        Log.d("image", image);
        Log.d("message", "before post");
        client.post(null, searchStr, params, new JsonHttpResponseHandler() {
            @Override
            public void onSuccess(int statusCode, cz.msebera.android.httpclient.Header[] headers,org.json.JSONObject response){
                //Log.d("message","successMessage");
                try {

                    if(response==null){
                        //display error message, not done
                        Log.d("message", "no results");
                    }
                    else {
                        String result=response.getString("url");
                        Log.d("message", result);

                        Uri uri = Uri.parse(result);
                        Intent intent = new Intent(Intent.ACTION_VIEW, uri);
                        startActivity(intent);

                    }
                } catch (final JSONException e) {
                    String result= null;
                    try {
                        result = response.getString("error");
                        Log.d("message", result);
                    } catch (JSONException e1) {
                        e1.printStackTrace();
                    }
                }
            }


        });
    }




}
