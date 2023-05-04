//Ya Hoo
using System;
using System.Collections.Generic;
using System.Text;
using System.Text.Json;
using System.IO;
using System.Linq;
using Newtonsoft.Json;
using Newtonsoft.Json.Serialization;
using Newtonsoft.Json.Linq;
using Newtonsoft.Json.Converters;
public class Program
{
    public static void Main()
    {
        string filename = @"C:\Users\ASUS\Desktop\UNI\TLA\Phase1\in\input2.json";
        string jsontext = File.ReadAllText(filename);
        var data = Newtonsoft.Json.JsonConvert.DeserializeObject<FA>(jsontext);
        var tra = Newtonsoft.Json.JsonConvert.DeserializeObject<dynamic>(jsontext);
        string s = data.states;
        string al = data.input_symbols;
        string initial = data.initial_state;
        string f = data.final_states;
        string trimed = tra.ToString();
        trimed = trimed.Replace(System.Environment.NewLine, "%");
        string [] xb = trimed.Split('%');
        List<State> states = new List<State>();
        List<string> alphabets = new List<string>();
        ReadJSONStates(s, states);
        ReadJSONAlphabets(al, alphabets);
        ReadJSONInit(initial, states);
        ReadJSONFinal(f, states);
        ReadJSONTransitions(xb,states);
        Queue<List<State>> dfa_states = new Queue<List<State>>();
        List<List<State>> final_dfa_states = new List<List<State>>();
        List<State> output = new List<State>();
        State TRAP = new State("TRAP");
        int trapflag = 0;
        List<State> init = new List<State>();
        init.Add(states[0]);
        //output.Add(q0);
        dfa_states.Enqueue(init);
        //int count = 0;
        while (dfa_states.Count > 0)
        {
            List<State> pstate = dfa_states.Dequeue();
            //Console.WriteLine(pstate[0].Name);
            List<State>[] tmp0 = new List<State>[alphabets.Count];
            final_dfa_states.Add(pstate);
            for (int jj = 0; jj < alphabets.Count; jj++) //# of alphabets
            {
               tmp0[jj] = new List<State>();
            }
            Lambda(pstate);
                for (int i = 0; i < pstate.Count; i++)
                    {   
                    for(int k = 0; k < pstate[i].transitions.Count; k++)
                    {
                        for (int l = 0; l < alphabets.Count; l++)
                        {
                            if (pstate[i].transitions[k].Name == alphabets[l] && IsCorrect(tmp0[l], pstate[i].transitions[k].destination))
                            {
                                tmp0[l].Add(pstate[i].transitions[k].destination);
                                    //Console.WriteLine(tmp0[l].Count);
                            }   
                        }   
                    }
                }
                for (int l = 0; l < alphabets.Count; l++)
                {
                    Lambda(tmp0[l]);
                }
                for (int l = 0; l < alphabets.Count; l++)
                    tmp0[l] = tmp0[l].OrderBy(a => a.Name).ToList();   
                  
                State Pstate = listToState(pstate);
                if(!IsThereAlready(pstate,output))
                    output.Add(listToState(pstate));
                //Console.WriteLine(Pstate.Name);
                //for(int i = 0; i < pstate.Count; i++)
                //Console.Write(pstate[i].Name + "");
                //Console.WriteLine();
                //Console.WriteLine(dfa_states[0].Count);
                //int co = 0;

            for (int e = 0; e < tmp0.Length; e++)
                {
                   
                    if (tmp0[e].Count > 0 && IsThereAlready(tmp0[e], output))
                    {
                        string name = "";
                        for (int i = 0; i < tmp0[e].Count; i++)
                        {
                            name += tmp0[e][i].Name;
                        }
                        for (int i2 = 0; i2 < output.Count; i2++)
                        {
                            if (name == output[i2].Name)
                            {
                            MakeTransition(output, Pstate, alphabets[e], output[i2]);
                            //Console.WriteLine(Pstate.Name + "-->" + output[i2].Name);
                            }
                        }
                    }
                    else if(tmp0[e].Count > 0)
                    {
                            output.Add(listToState(tmp0[e]));

                            MakeTransition(output, Pstate, alphabets[e], output[output.Count - 1]);
                            dfa_states.Enqueue(tmp0[e]);
                            //Console.WriteLine(Pstate.Name + "-->" + output[output.Count - 1].Name);
                    }
                    else //TRAP
                    {
                        if (trapflag == 0)
                            output.Add(TRAP);
                        trapflag = 1;
                        MakeTransition(output, Pstate, alphabets[e], TRAP);
                    }
            }
        }
        if(trapflag == 1)
        {
            for(int e = 0; e < alphabets.Count; e++)
                MakeTransition(output, TRAP, alphabets[e], TRAP);
        }

        WriteJSONS(@"C:\Users\ASUS\Desktop\UNI\TLA\Phase1\out\x.json", output,alphabets,states);
        for (int i = 0; i < output.Count; i++)
        {
            Console.WriteLine(output[i].Name);
            for(int a = 0; a < output[i].transitions.Count; a++)
            {
                Console.WriteLine(output[i].transitions[a].Name + " " + output[i].transitions[a].destination.Name);
            }
        }
       
    }
    public static bool IsThereAlready(List<State> tmp0, List<State> final_dfa_states)
    {
        string name = "";
        for(int i = 0; i < tmp0.Count; i++)
        {
            name += tmp0[i].Name;
        }
        for (int i = 0; i < final_dfa_states.Count; i++)
        {
            if (name == final_dfa_states[i].Name)
                return true;
        }
        return false;
    }
    public static bool IsCorrect(List<State> states, State x)
    {
        for (int i = 0; i < states.Count; i++)
            if (states[i].Name.Contains(x.Name) || x.Name.Contains(states[i].Name))
                return false;
        return true;
    }
    public static State listToState(List<State> states)
    {
        string na = "";
        for (int i = 0; i < states.Count; i++)
        {
            na += states[i].Name;
        }
        return new State(na);
    }
    public static void MakeTransition(List<State> output, State Pstate, string alph, State des)
    {
        for (int i = 0; i < output.Count; i++)
            if (output[i].Name == Pstate.Name)
                output[i].transitions.Add(new transition(alph, des));
    }
    public static void Lambda(List<State> pstate)
    {
        for (int i = 0; i < pstate.Count; i++)
        {
            for (int k = 0; k < pstate[i].transitions.Count; k++)
            {
                if (pstate[i].transitions[k].Name == "" && IsCorrect(pstate, pstate[i].transitions[k].destination))
                {
                    pstate.Add(pstate[i].transitions[k].destination);
                }
            }
        }
        pstate = pstate.OrderBy(x => x.Name).ToList();
    }
    public static void ReadJSONStates(string s, List<State> states)
    {
        string[] s2 = s.Split(',');
        for (int i = 0; i < s2.Length; i++)
        {
            states.Add(new State(s2[i].Trim('{', '\'', '\'', '}')));
        }
    }
    public static void ReadJSONAlphabets(string s, List<string> alp)
    {
        string[] s2 = s.Split(',');
        for (int i = 0; i < s2.Length; i++)
        {
            alp.Add(s2[i].Trim('{', '\'', '\'', '}'));
        }
    }
    public static void ReadJSONTransitions(string[] xb, List<State> states)
    {
        for (int i = 4; i < xb.Length; i++)
        {
            string st = "";
            if (xb[i].Contains(": {"))
            {
                st = xb[i].Trim(' ', '{', ':', '"');
                int j = i + 1;
                //string alp = "";
                //string to_state = "";
                while (!xb[j].Contains("},") && !xb[j].Contains(": {") && xb[j].Trim() != "}")
                {
                    string[] op = xb[j].Split(':');
                    j++;
                    string [] to = op[1].Split(',');
                    for (int p = 0; p < to.Length; p++)
                    {
                        for (int k = 0; k < states.Count; k++)
                        {
                            if (states[k].Name == st)
                            {
                                for (int y = 0; y < states.Count; y++)
                                {
                                    if (states[y].Name == to[p].Trim('"', '{', '}', '\'', ',', ' '))
                                        states[k].transitions.Add(new transition(op[0].Trim('"', ' '), states[y]));
                                }
                            }
                        }
                    }
                    
                }
            }
        }
    }
    public static void ReadJSONInit(string s, List<State> states)
    {
            string q = s.Trim('{', '\'', '\'', '}');
            for(int i = 0; i < states.Count; i++)
                if(states[i].Name == q)
                    states[i].IsInitial = true;
    }
    public static void ReadJSONFinal(string s, List<State> states)
    {
        string[] s2 = s.Split(',');
        for (int i = 0; i < s2.Length; i++)
        {
            s2[i] = s2[i].Trim('{', '\'', '\'', '}');
        }
        for (int i = 0; i < s2.Length; i++)
        {
            for(int j = 0; j < states.Count; j++)
                if(states[j].Name == s2[i])
                    states[j].IsFinal = true;
        }
    }
    public static void WriteJSONS(string Filename, List<State> output, List<string> alp, List<State> states)
    {
        string a = "";
        a += "{" + "\n";
        a += "\"states\": \"{";
        for (int i = 0; i < output.Count; i++)
        {
           a += "'" + output[i].Name + "'";
            if (i < output.Count - 1)
                a += ",";
            else
                a += "}\"," + "\n"; 
        }
        a += "\"input_symbols\": \"{";
        for(int i = 0; i < alp.Count; i++)
        {
            a += "'" + alp[i] + "'";
            if (i < alp.Count - 1)
                a += ",";
            else
                a += "}\"," + "\n";
        }
        a += "\"transitions\": {" + "\n";
        for (int i = 0; i < output.Count; i++)
        {
            a += "\"" + output[i].Name + "\": {" + "\n";
            for(int j = 0; j < output[i].transitions.Count; j++)
            {
                a += "\"" + output[i].transitions[j].Name + "\": " + "\"" + output[i].transitions[j].destination.Name + "\"";
                if (j < output[i].transitions.Count - 1)
                    a += "," + "\n";
                else
                {
                    a += "\n" + "}";
                    if (i < output.Count - 1)
                        a += "," + "\n";
                    else
                        a += "\n" + "}," + "\n";
                }
            }
        }
        a += "\"initial_state\": \""; 
        for(int i = 0;i < output.Count; i++)
        {
            for (int j = 0; j < states.Count; j++)
                if (states[j].IsInitial && output[i].Name.Contains(states[j].Name))
                    a += output[i].Name;
        }
        a += "\"," + "\n";
        a += "\"final_states\": \"{";
        for (int i = 0; i < output.Count; i++)
        {
            for (int j = 0; j < states.Count; j++)
                if (states[j].IsFinal && output[i].Name.Contains(states[j].Name))
                {
                    a += "'" + output[i].Name + "',";
                    break;
                }
        }
        a = a.TrimEnd(',' , ' ');
        a += "}\"" + "\n" + "}";
        File.WriteAllText(Filename, a);
    }
}
public class FA
{
    public string states { get; set; }
    public string input_symbols { get; set; }
    public string initial_state { get; set; }
    public string final_states { get; set; }
}
public class State
{
    public string Name { get; set; }
    public bool IsFinal { get; set; }
    public bool IsInitial { get; set; }
    public List<transition> transitions { get; set; }
    public State(string name)
    {
        this.Name = name;
        this.transitions = new List<transition>();
    }
}
public class transition
{
    public string Name { get; set; }
    public State destination { get; set; }
    public transition(string alph, State d)
    {
        this.Name = alph;
        this.destination = d;
    }
}
