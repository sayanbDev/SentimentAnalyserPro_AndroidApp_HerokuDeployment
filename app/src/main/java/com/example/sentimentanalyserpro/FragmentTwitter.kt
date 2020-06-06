package com.example.sentimentanalyserpro


import android.os.Bundle
import android.util.Log
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.fragment.app.Fragment
import com.android.volley.*
import com.android.volley.toolbox.JsonObjectRequest
import com.android.volley.toolbox.Volley
import kotlinx.android.synthetic.main.fragment_twitter.view.*
import org.json.JSONException
import org.json.JSONObject


/**
 * A simple [Fragment] subclass.
 */
class FragmentTwitter : Fragment() {
    private lateinit var mQueue:RequestQueue

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        val view = inflater.inflate(R.layout.fragment_twitter, container, false)
        mQueue = Volley.newRequestQueue(activity)
        view.btnAnalyse2.setOnClickListener {
            Log.i(activity.toString(), "button was clicked")
            loginUser()

        }
        return view
    }
//    private fun jsonParse(){
//        val url = "http://10.0.2.2:5000/api/post_some_data"
//        val request =
//            JsonObjectRequest(
//                Request.Method.GET, url, null,
//                Response.Listener { response ->
//                    try {
//                        se  = response.getString("overall")
//                        Log.i(activity.toString(),response.toString())
//                        view?.textView2!!.text="Overall Sentiment Of topic Iphone is : "+se
//
//
//                    } catch (e: JSONException) {
//                        e.printStackTrace()
//                    }
//                }, Response.ErrorListener { error -> error.printStackTrace() })
//        request.retryPolicy=
//            DefaultRetryPolicy(60000, DefaultRetryPolicy.DEFAULT_MAX_RETRIES, DefaultRetryPolicy.DEFAULT_BACKOFF_MULT)
//        mQueue.add(request)
//    }
    private fun loginUser() {
    val url = "http://10.0.2.2:5000/api/post_some_data"
    val params = HashMap<String,String>()
    params["topic"] = view?.textToAnalyze2!!.text.toString()
    params["no"] = view?.textToAnalyze3!!.text.toString()
    val reqJson = JSONObject(params as Map<*, *>)


    val request =
            JsonObjectRequest(
                Request.Method.POST, url, reqJson,
                Response.Listener { response ->
                    try {
                        val se  = response.getString("overall")
                        val sentiments="positive % = "
                        Log.i(activity.toString(),response.toString())
                        view?.textView2!!.text="Overall Sentiment Of "+response.getString("search")+" in "+response.getString("no_of_tweets")+" no of tweets is : "+se


                    } catch (e: JSONException) {
                        e.printStackTrace()
                    }
                }, Response.ErrorListener { error -> error.printStackTrace() })
        request.retryPolicy=
            DefaultRetryPolicy(50000000, DefaultRetryPolicy.DEFAULT_MAX_RETRIES, DefaultRetryPolicy.DEFAULT_BACKOFF_MULT)
        mQueue.add(request)
    }
}

