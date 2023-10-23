import React, { useState } from 'react'
import { Grid, Paper, TextField, Button } from '@mui/material'
import useLogin from '../hooks/useLogin'

function Login() {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const {login, error, isLoading} = useLogin()

  const handleSubmit = async (e) => {
    e.preventDefault()
    console.log("login", username, password)
    await login(username, password)
  }

  const paperStyle={padding:20,height:360,width:300, margin:'20px auto'}
  const txtstyle={margin:'8px 0'}
  const btnstyle={margin:'10px 0'}
  const errstyle={
    padding: '5px',
    background: '#ffefef',
    border: '1px solid #e7195a',
    color: '#e7195a',
    margin: '10px 0'
  }

  return (
    <Grid>
      <Paper elevation={10} style={paperStyle}>
        <Grid align='center'>
          <h2>Login</h2>
        </Grid>
        <form onSubmit={ handleSubmit } >
          <TextField 
            label='Username' 
            placeholder='Enter username' 
            fullWidth 
            required
            style={txtstyle}
            value={username}
            onChange={ (e) => setUsername(e.target.value)}
          />
          <TextField 
            label='Password' 
            placeholder='Enter password' 
            type='password' 
            fullWidth 
            required
            value={password}
            onChange={ (e) => setPassword(e.target.value)}
          />
          <Button 
            type='submit'
            color='primary'
            variant="contained"
            style={btnstyle}
            fullWidth
            disabled={isLoading}
          >
            Login
          </Button>
          {error && <div style={errstyle}>{error}</div>}
        </form>
      </Paper>
    </Grid>
  )
}

export default Login